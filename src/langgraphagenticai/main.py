from src.langgraphagenticai.ui.streamlitui.loadui import LoadStreamlitUI
from src.langgraphagenticai.LLMs.groqllm import GROQLLM
from src.langgraphagenticai.graph.graph_builder import GraphBuilder
from src.langgraphagenticai.ui.streamlitui.display_result import DisplayResultStreamlit
import streamlit as st
import uuid
from langgraph.checkpoint.memory import MemorySaver


def load_langgraph_agenticai_app():
    """Loads and runs the Langgraph Agentic AI application with streamlitUI
    """

    #Load UI
    ui= LoadStreamlitUI()
    user_input = ui.load_streamlit_ui()

    if "memory" not in st.session_state:
        st.session_state.memory = MemorySaver()

    if "thread_id" not in st.session_state:
        st.session_state.thread_id = str(uuid.uuid4())

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    if not user_input:
        return st.error("Error: Failed to load user input from the UI")
         
    if st.session_state.IsFetchButtonClicked:
        user_message = st.session_state.timeframe
    else:
        user_message = st.chat_input("Enter your message:")

    if user_message:
        try:
            st.session_state.chat_history.append({"role": "user", "content": user_message})
            with st.chat_message("user"):
                st.write(user_message)
            obj_llm_config = GROQLLM(user_controls_input = user_input)
            model = obj_llm_config.get_llm_models()

            if not model:
                st.error("Error:LLM model could not be initialized")
                return
            
            #Intialise the graph based on usecases
            usecase = user_input.get("selected_usecase")

            #graph builder
            graph_builder = GraphBuilder(model,st.session_state.memory)
            config = {"configurable": {"thread_id": st.session_state.thread_id}}
            try:
                graph = graph_builder.setup_graph(usecase)
                DisplayResultStreamlit(usecase,graph,user_message,config).display_result_on_ui()
            except Exception as e:
                st.error(f"Error: Graph setup failed - {e}")
        
        except Exception as e:
            st.error("Setup Failed")
            return





