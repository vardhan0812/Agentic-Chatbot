# End-to-End Agentic AI Chatbot

This project is a Streamlit-based LangGraph app that supports three use cases:

- `Chatbot`: a basic Groq-powered conversational assistant
- `Chatbot With Web`: a chatbot that can use Tavily-backed web search tools
- `AI News`: a small AI news explorer that fetches news, summarizes it with an LLM, and saves the result as markdown

## Tech Stack

- Python
- Streamlit
- LangGraph
- LangChain Core / Community
- Groq via `langchain-groq`
- Tavily Search

## Features

- Sidebar-driven UI for provider, model, and use case selection
- Groq model selection from config
- Tool-enabled chatbot graph
- AI news fetch and summarization workflow
- Markdown news summaries saved under `AINews/`

## Project Structure

```text
.
├── app.py
├── requirements.txt
├── AINews/
├── src/
│   └── langgraphagenticai/
│       ├── main.py
│       ├── graph/
│       │   └── graph_builder.py
│       ├── LLMs/
│       │   └── groqllm.py
│       ├── nodes/
│       │   ├── ai_news_node.py
│       │   ├── basic_chatbot_node.py
│       │   └── chatbot_with_tool_node.py
│       ├── state/
│       │   └── state.py
│       ├── tools/
│       │   └── search_tool.py
│       └── ui/
│           ├── uiconfigfile.ini
│           ├── uiconfigfile.py
│           └── streamlitui/
│               ├── loadui.py
│               └── display_result.py
```

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the Streamlit app:

```bash
streamlit run app.py
```

## API Keys

This project uses:

- `GROQ_API_KEY`
- `TAVILY_API_KEY` for `Chatbot With Web` and `AI News`

You can enter these directly from the Streamlit sidebar.

## Use Cases

### 1. Chatbot

Choose:

- Provider: `Groq`
- A model from the dropdown
- Use case: `Chatbot`

Then type in the chat box to get a basic assistant response.

### 2. Chatbot With Web

Choose:

- Use case: `Chatbot With Web`
- Enter your Tavily API key in the sidebar

This flow uses a LangGraph tool node plus a chatbot node to answer with tool-assisted results.

### 3. AI News

Choose:

- Use case: `AI News`
- Enter your Tavily API key
- Select a time frame: `Daily`, `Weekly`, or `Monthly`
- Click `Fetch latest AI News`

The app:

1. fetches AI news using Tavily
2. summarizes the results using the selected LLM
3. saves markdown summaries in the `AINews/` folder
4. renders the generated markdown in Streamlit

## Configuration

UI options are defined in:

- `src/langgraphagenticai/ui/uiconfigfile.ini`

This includes:

- page title
- supported LLM providers
- supported use cases
- Groq model options

## Notes

- The current app is configured around Groq in the UI.
- AI News summaries are written to files like `AINews/daily_summary.md` and `AINews/weekly_summary.md`.
- The app uses LangGraph state for message passing and graph execution.
