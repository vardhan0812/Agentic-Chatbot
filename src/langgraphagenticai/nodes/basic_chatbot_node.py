from src.langgraphagenticai.state.state import State

class BasicChatbotNode:
    """CHATBOT logic implementation
    """
    def __init__(self,model):
        self.llm= model

    def process(self,state:State)->dict:
        """Process input state and return response"""
        return {"messages":self.llm.invoke(state["messages"])}

    