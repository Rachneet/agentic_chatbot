from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition

from src.agentic_ai.state.graph_state import GraphState
from src.agentic_ai.nodes.basic_chatbot_node import BasicChatbotNode
from src.agentic_ai.nodes.chatbot_with_tools_node import ChatbotWithToolsNode
from src.agentic_ai.nodes.news_node import NewsNode
from src.agentic_ai.tools.search_tool import get_tools, create_tool_node


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


    def chatbot_with_tools_graph(self):
        """
        Build a chatbot with tools integration.

        """
        tools = get_tools()
        tool_node = create_tool_node(tools)

        # node functionality
        self.chatbot_with_tools_node = ChatbotWithToolsNode(self.model)
        chatbot_node_with_tools = self.chatbot_with_tools_node.process(tools)

        # nodes
        self.graph_builder.add_node(
            "chatbot",
            chatbot_node_with_tools,
        )
        self.graph_builder.add_node(
            "tools",
            tool_node,
        )

        # edges
        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_conditional_edges(
            "chatbot", 
            tools_condition
            )
        self.graph_builder.add_edge("tools", "chatbot")
        self.graph_builder.add_edge("chatbot", END)

    
    def chatbot_with_news_agent_graph(self):
        """
        Build a chatbot with news agent integration.

        """

        # node functionality
        self.news_node = NewsNode(self.model)

        # nodes
        self.graph_builder.add_node(
            "fetch_news",
            self.news_node.fetch_news
        )
        self.graph_builder.add_node(
            "summarizer",
            self.news_node.summarize_news
        )
        self.graph_builder.add_node(
            "save_results",
            self.news_node.save_results
        )

        # edges
        self.graph_builder.set_entry_point("fetch_news")
        self.graph_builder.add_edge("fetch_news", "summarizer")
        self.graph_builder.add_edge("summarizer", "save_results")
        self.graph_builder.add_edge("save_results", END)

    
    def setup_graph(self, use_case: str):
        """
        Which graph to set up based on use case.
        """
        if use_case == "Basic Chatbot":
            self.basic_chatbot_graph()
        elif use_case == "Chatbot with Tools":
            self.chatbot_with_tools_graph()
        elif use_case == "News Agent":
            self.chatbot_with_news_agent_graph()

        return self.graph_builder.compile()