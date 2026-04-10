# End-to-End Agentic Chatbot

This project is a Streamlit-based LangGraph app that supports three use cases:

- `Chatbot`: a Groq-powered conversational assistant with multi-turn memory
- `Chatbot With Web`: a chatbot that can use Tavily-backed web search tools with multi-turn memory
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
- Multi-turn conversation memory for chat use cases
- Tool-enabled chatbot graph
- AI news fetch and summarization workflow
- Markdown news summaries saved under `AINews/`

## How Memory Works

The `Chatbot` and `Chatbot With Web` flows support multi-turn memory in the current Streamlit session.

This is implemented using:

- LangGraph state with `messages: Annotated[list, add_messages]`
- `MemorySaver` as the LangGraph checkpointer
- a per-session `thread_id`
- `st.session_state` to persist the active `thread_id` and checkpointer object across Streamlit reruns

This allows the chatbot to remember previous user and assistant turns during an active session.

## Project Structure

```text
.
|-- app.py
|-- requirements.txt
|-- README.md
|-- AINews/
|-- src/
|   `-- langgraphagenticai/
|       |-- main.py
|       |-- graph/
|       |   `-- graph_builder.py
|       |-- LLMs/
|       |   `-- groqllm.py
|       |-- nodes/
|       |   |-- ai_news_node.py
|       |   |-- basic_chatbot_node.py
|       |   `-- chatbot_with_tool_node.py
|       |-- state/
|       |   `-- state.py
|       |-- tools/
|       |   `-- search_tool.py
|       `-- ui/
|           |-- uiconfigfile.ini
|           |-- uiconfigfile.py
|           `-- streamlitui/
|               |-- loadui.py
|               `-- display_result.py
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

Then type in the chat box to get a basic assistant response. This flow supports multi-turn conversation memory in the active session.

### 2. Chatbot With Web

Choose:

- Use case: `Chatbot With Web`
- Enter your Tavily API key in the sidebar

This flow uses a LangGraph tool node plus a chatbot node to answer with tool-assisted results, and it retains conversation context during the active session.

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
- For prototype deployment, the `AINews/` folder is being used as temporary runtime storage for generated markdown files.
