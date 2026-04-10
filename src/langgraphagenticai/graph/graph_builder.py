from langgraph.graph import StateGraph,START,END
from src.langgraphagenticai.state.state import State
from src.langgraphagenticai.nodes.basic_chatbot_node import BasicChatbotNode
from src.langgraphagenticai.tools.search_tool import get_tools
from src.langgraphagenticai.tools.search_tool import create_tool_node
from langgraph.prebuilt import tools_condition
from src.langgraphagenticai.nodes.chatbot_with_tool_node import ChatbotWithToolNode 

class GraphBuilder:
    def __init__(self,model):
        self.llm = model
        self.graph_builder = StateGraph(State)

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


    def setup_graph(self,usecase):
        """set up the graph for the selected usecase"""

        if usecase == "Chatbot":
            self.basic_chatbot_build_graph()
        if usecase == "Chatbot With Web":
            self.chatbot_with_tools_build_graph()

        return self.graph_builder.compile()
