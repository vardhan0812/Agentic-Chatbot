from src.langgraphagenticai.ui.streamlitui.loadui import LoadStreamlitUI
import streamlit as st

def load_langgraph_agenticai_app():
    """Loads and runs the Langgraph Agentic AI application with streamlitUI
    """

    #Load UI
    ui= LoadStreamlitUI()
    user_input = ui.load_streamlit_ui()

    if not user_input:
        return st.error("Error: Failed to load user input from the UI")
         
    
    user_message = st.chat_input("Enter your message:")

    if user_message:
        pass

