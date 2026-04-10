from langgraph.graph import StateGraph,START,END
from src.langgraphagenticai.state.state import State
from src.langgraphagenticai.nodes.basic_chatbot_node import BasicChatbotNode
from src.langgraphagenticai.tools.search_tool import get_tools
from src.langgraphagenticai.tools.search_tool import create_tool_node
from langgraph.prebuilt import tools_condition
from src.langgraphagenticai.nodes.chatbot_with_tool_node import ChatbotWithToolNode 
from src.langgraphagenticai.nodes.ai_news_node import AINewsNode
from langgraph.checkpoint.memory import MemorySaver

class GraphBuilder:
    def __init__(self,model,memory):
        self.llm = model
        self.graph_builder = StateGraph(State)
        self.memory = memory

    def basic_chatbot_build_graph(self):
        """Builds a chatbot using langgraph"""

        self.basic_chatbot_node = BasicChatbotNode(self.llm)

        self.graph_builder.add_node("chatbot",self.basic_chatbot_node.process)
        self.graph_builder.add_edge(START,"chatbot")
        self.graph_builder.add_edge("chatbot",END)

    def chatbot_with_tools_build_graph(self):
        """Builds an advanced chatbot graph with tool integration, this has both a chatbot node and a tool node"""
        ## Define the tool and tool node
        tools = get_tools()
        tool_node=create_tool_node(tools)

        #define llm
        llm=self.llm

        #define chatbot node
        obj_chatbot_with_node = ChatbotWithToolNode(llm)
        chatbot_node = obj_chatbot_with_node.create_chatbot(tools)

        #add node
        self.graph_builder.add_node("chatbot",chatbot_node)
        self.graph_builder.add_node("tools",tool_node)

        #add edges
        self.graph_builder.add_edge(START,"chatbot")
        self.graph_builder.add_conditional_edges("chatbot",tools_condition)
        self.graph_builder.add_edge("tools","chatbot")
        self.graph_builder.add_edge("chatbot",END)

    def ai_news_builder_graph(self):
        ai_news_node = AINewsNode(self.llm)
               
        self.graph_builder.add_node("fetch_news",ai_news_node.fetch_news) #type:ignore
        self.graph_builder.add_node("summerize_news",ai_news_node.summerize_news) #type:ignore
        self.graph_builder.add_node("save_result",ai_news_node.save_result)

        self.graph_builder.add_edge(START,"fetch_news")
        self.graph_builder.add_edge("fetch_news","summerize_news")
        self.graph_builder.add_edge("summerize_news","save_result")
        self.graph_builder.add_edge("save_result",END)


    def setup_graph(self,usecase):
        """set up the graph for the selected usecase"""

        if usecase == "Chatbot":
            self.basic_chatbot_build_graph()
        if usecase == "Chatbot With Web":
            self.chatbot_with_tools_build_graph()
        if usecase == "AI News":
            self.ai_news_builder_graph()

        return self.graph_builder.compile(checkpointer=self.memory)
