import streamlit as st
import os

from src.langgraphagenticai.ui.uiconfigfile import Config

class LoadStreamlitUI:
    def __init__(self):
        self.config = Config()
        self.user_controls = {}

    def load_streamlit_ui(self):
        st.set_page_config(page_title=self.config.get_page_title(),layout="wide")
        st.markdown(
            """
            <style>
                .stApp {
                    background:
                        radial-gradient(circle at top right, rgba(255, 166, 0, 0.10), transparent 24%),
                        radial-gradient(circle at top left, rgba(255, 59, 48, 0.09), transparent 20%),
                        linear-gradient(180deg, #0d1117 0%, #11151d 100%);
                }

                section[data-testid="stSidebar"] {
                    background: linear-gradient(180deg, #232630 0%, #1b1f28 100%);
                    border-right: 1px solid rgba(255, 255, 255, 0.06);
                }

                [data-testid="stChatMessage"] {
                    border: 1px solid rgba(255, 255, 255, 0.06);
                    border-radius: 18px;
                    background: rgba(255, 255, 255, 0.03);
                    box-shadow: 0 14px 34px rgba(0, 0, 0, 0.18);
                    backdrop-filter: blur(4px);
                    margin-bottom: 0.75rem;
                }

                [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
                    background: linear-gradient(180deg, rgba(255, 88, 66, 0.12), rgba(255, 88, 66, 0.05));
                }

                [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
                    background: linear-gradient(180deg, rgba(255, 184, 0, 0.14), rgba(255, 184, 0, 0.05));
                }

                .agent-shell {
                    padding: 0.25rem 0 1rem 0;
                }

                .agent-eyebrow {
                    color: #ffb000;
                    text-transform: uppercase;
                    letter-spacing: 0.18em;
                    font-size: 0.78rem;
                    font-weight: 700;
                    margin-bottom: 0.4rem;
                }

                .agent-title {
                    font-size: 3rem;
                    line-height: 1;
                    font-weight: 800;
                    margin: 0;
                    color: #fff7e6;
                }

                .agent-subtitle {
                    margin-top: 0.55rem;
                    color: #b9c2d0;
                    max-width: 42rem;
                    font-size: 1rem;
                }

                .stChatInputContainer {
                    background: rgba(17, 21, 29, 0.92);
                }
            </style>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            f"""
            <div class="agent-shell">
                <div class="agent-eyebrow">Conversational Workspace</div>
                <h1 class="agent-title">{self.config.get_page_title()}</h1>
                <div class="agent-subtitle">A memory-enabled LangGraph assistant with tool use and AI news workflows.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if "timeframe" not in st.session_state:
            st.session_state.timeframe = ""
        if "IsFetchButtonClicked" not in st.session_state:
            st.session_state.IsFetchButtonClicked = False

        with st.sidebar:
            llm_options = self.config.get_llm_options()
            usecase_options = self.config.get_usecase_options()

            self.user_controls["selected_llm"] = st.selectbox("Select Provider",llm_options)

            if self.user_controls["selected_llm"] == 'Groq':
                model_options = self.config.get_groq_model_options()
                self.user_controls["selected_groq_model"]=st.selectbox("Select Model",model_options)
                self.user_controls["GROQ_API_KEY"] = st.session_state["GROQ_API_KEY"]=st.text_input("API Key", type = "password")

                if not self.user_controls["GROQ_API_KEY"]:
                    st.warning("Please enter your GROQ API key to proceed.")

            #Use case selection
            self.user_controls["selected_usecase"]=st.selectbox("Select Usecase",usecase_options)

            if self.user_controls["selected_usecase"] == "Chatbot With Web":
                os.environ["TAVILY_API_KEY"]=self.user_controls["TAVILY_API_KEY"] = st.session_state["TAVILY_API_KEY"] = st.text_input("TAVILY API KEY",type="password")
                if not self.user_controls["TAVILY_API_KEY"]:
                    st.warning("Please Enter your Tavily api key to proceed.")

            if self.user_controls["selected_usecase"] == "AI News":
                os.environ["TAVILY_API_KEY"]=self.user_controls["TAVILY_API_KEY"] = st.session_state["TAVILY_API_KEY"] = st.text_input("TAVILY API KEY",type="password")
                st.subheader("AI News Explorer")
                with st.sidebar:
                    time_frame = st.selectbox("Select Time Frame",["Daily","Weekly","Monthly"],index=0)

                if st.button("Fetch latest AI News",use_container_width=True):
                    st.session_state.IsFetchButtonClicked = True
                    st.session_state.timeframe = time_frame



                if not self.user_controls["TAVILY_API_KEY"]:
                    st.warning("Please Enter your Tavily api key to proceed.")

        return self.user_controls










