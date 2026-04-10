import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
import json
import time
import uuid


class DisplayResultStreamlit:
    def __init__(self, usecase, graph, user_message,config):
        self.usecase = usecase
        self.graph = graph
        self.user_message = user_message
        self.config = config

    def _typewriter(self, text, delay=0.012):
        placeholder = st.empty()
        typed_text = ""

        for char in text:
            typed_text += char
            placeholder.markdown(typed_text + "▌")
            time.sleep(delay)

        placeholder.markdown(typed_text)

    def display_result_on_ui(self):
        usecase = self.usecase
        graph = self.graph
        user_message = self.user_message
        config = self.config

        if usecase == "Chatbot":
            assistant_reply = None

            for event in graph.stream({"messages": ("user", user_message)}, config=config):
                print(event.values())
                for value in event.values():
                    print(value["messages"])
                    assistant_reply = value["messages"].content

            if assistant_reply:
                st.session_state.chat_history.append({"role": "assistant", "content": assistant_reply})
                with st.chat_message("assistant"):
                    self._typewriter(assistant_reply)

                    
        elif usecase == "Chatbot With Web":
            # Prepare state and invoke the graph
            initial_state = {"messages": [("user", user_message)]}
            res = graph.invoke(initial_state,config=config)
            latest_assistant_reply = None

            for message in res["messages"]:
                if type(message) == HumanMessage:
                    continue

                elif type(message) == ToolMessage:
                    continue

                elif type(message) == AIMessage and message.content:
                    latest_assistant_reply = message.content

            if latest_assistant_reply:
                st.session_state.chat_history.append({"role": "assistant", "content": latest_assistant_reply})
                with st.chat_message("assistant"):
                    self._typewriter(latest_assistant_reply)

        elif usecase == "AI News":
            frequency = self.user_message
            with st.spinner("Fetching and summarizing news...⏳"):
                result = graph.invoke(
                    {"messages": [("user", frequency)]},
                    config={"configurable": {"thread_id": str(uuid.uuid4())}},
                )
                try:
                    # Read the markdown file
                    AI_NEWS_PATH = f"./AINews/{frequency.lower()}_summary.md"
                    with open(AI_NEWS_PATH, "r") as file:
                        markdown_content = file.read()

                    # Display the markdown content in Streamlit
                    st.markdown(markdown_content, unsafe_allow_html=True)
                except FileNotFoundError:
                    st.error(f"News Not Generated or File not found: {AI_NEWS_PATH}")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
