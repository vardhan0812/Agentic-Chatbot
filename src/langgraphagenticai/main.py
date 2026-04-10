from src.langgraphagenticai.ui.streamlitui.loadui import LoadStreamlitUI
from src.langgraphagenticai.LLMs.groqllm import GROQLLM
from src.langgraphagenticai.graph.graph_builder import GraphBuilder
from src.langgraphagenticai.ui.streamlitui.display_result import DisplayResultStreamlit
import streamlit as st

def load_langgraph_agenticai_app():
    """Loads and runs the Langgraph Agentic AI application with streamlitUI
    """

    #Load UI
    ui= LoadStreamlitUI()
    user_input = ui.load_streamlit_ui()

    if not user_input:
        return st.error("Error: Failed to load user input from the UI")
         
    if st.session_state.IsFetchButtonClicked:
        user_message = st.session_state.timeframe
    else:
        user_message = st.chat_input("Enter your message:")

    if user_message:
        try:
            obj_llm_config = GROQLLM(user_controls_input = user_input)
            model = obj_llm_config.get_llm_models()

            if not model:
                st.error("Error:LLM model could not be initialized")
                return
            
            #Intialise the graph based on usecases
            usecase = user_input.get("selected_usecase")

            #graph builder
            graph_builder = GraphBuilder(model)

            try:
                graph = graph_builder.setup_graph(usecase)
                DisplayResultStreamlit(usecase,graph,user_message).display_result_on_ui()
            except Exception as e:
                st.error(f"Error: Graph setup failed - {e}")
        
        except Exception as e:
            st.error("Setup Failed")
            return





