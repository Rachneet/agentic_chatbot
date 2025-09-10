from langgraph.graph import StateGraph, START, END

from src.agentic_ai.state.graph_state import GraphState
from src.agentic_ai.nodes.basic_chatbot_node import BasicChatbotNode


class GraphBuilder:
    def __init__(self, model):
        self.model = model
        self.graph_builder = StateGraph(GraphState)


    def basic_chatbot_graph(self):
        """
        Build a basic chatbot using LangGraph.
        """

        self.basic_chatbot_node = BasicChatbotNode(self.model)

        # nodes
        self.graph_builder.add_node(
            "chatbot",
            self.basic_chatbot_node.process,
        )

        # edges
        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_edge("chatbot", END)

    
    def setup_graph(self, use_case: str):
        """
        Which graph to set up based on use case.
        """
        if use_case == "Basic Chatbot":
            self.basic_chatbot_graph()

        return self.graph_builder.compile()