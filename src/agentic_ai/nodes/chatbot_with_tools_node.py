from src.agentic_ai.state.graph_state import GraphState
from src.agentic_ai.models.groqllm import GroqLLM


class ChatbotWithToolsNode:
    """
    A chatbot node that integrates with external tools.
    """
    def __init__(self, model):
        self.model = model

    def process(self, tools):
        """
        Create a chatbot with the specified tools.
        """
        
        model_with_tools = self.model.bind_tools(tools)

        def chatbot_node(state: GraphState):
            """
            Chatbot logic for processing the input state and returning a response.
            """
            return {
            "messages": model_with_tools.invoke(state["messages"])
            }
        return chatbot_node
