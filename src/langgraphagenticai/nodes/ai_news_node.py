from tavily import TavilyClient
from langchain_core.prompts import ChatPromptTemplate

class AINewsNode:
    def __init__(self,llm):
        """Intialsie the ainewsnode with api keys"""

        self.tavily = TavilyClient()
        self.llm = llm
        self.state={} #used to capture various state
    

    def fetch_news(self,state:dict)->dict:
        """Fetch AI News based on specified frequency
        
        Args:
        state: the dictionary containing frequency

        Returns:
        dict: Updated state with "news_data" key containing fetched news
        """

        frequency = state["messages"][0].content.lower()
        self.state['frequency'] = frequency
        time_range_map = {'daily':'d','weekly':'w','monthly':'m','year':'y'}
        days_map = {'daily':1,'weekly':7,'monthly':30,'year':365}

        response = self.tavily.search(
            query="AI news with most impact globally",
            topic="news",
            time_range= time_range_map[frequency],  # type: ignore
            include_answer="advanced",
            max_results=20,
            days=days_map[frequency]
        )

        state['news_data'] = response.get('results',[])
        self.state['news_data']=state['news_data']
        return state


    def summerize_news(self,state:dict)->dict:
        """Summerizes the fetched news using llm"""

        news_items = self.state['news_data']

        prompt_template = ChatPromptTemplate.from_messages([
            ("system", """You are an AI news editor.

        Convert the provided AI news articles into clean markdown.

        Rules:
        1. Group articles by date in **YYYY-MM-DD** format.
        2. Under each date, write bullet points.
        3. Each bullet must contain:
        - one short summary sentence in your own words
        - then a markdown link exactly in this format: [Read more](URL)
        4. Do not output raw headlines as the whole bullet.
        5. Do not copy article titles unless absolutely necessary.
        6. Keep each bullet concise and informative.
        7. Sort dates from latest to oldest.

        Output example:
        ### 2025-06-05
        - AI adoption is helping traditional companies improve productivity and business efficiency. [Read more](https://example.com)

        ### 2025-06-04
        - New AI-focused startups are building tools for workforce and business transformation. [Read more](https://example.com)
        """),
            ("user", "Articles:\n{articles}")
        ])


        articles_str = "\n\n".join([
            f"Content: {item.get('content', '')}\nURL: {item.get('url', '')}\nDate: {item.get('published_date', '')}"
            for item in news_items
        ])

        response = self.llm.invoke(prompt_template.format(articles=articles_str))
        state['summary'] = response.content
        self.state["summary"]=state['summary']
        return self.state

    def save_result(self, state):
        frequency = self.state['frequency']
        summary = self.state['summary']
        filename = f"./AINews/{frequency}_summary.md"

        with open(filename, 'w') as f:
            f.write(f"# {frequency.capitalize()} AI News Summary\n\n")
            f.write(summary)

        self.state['filename'] = filename
        return self.state


