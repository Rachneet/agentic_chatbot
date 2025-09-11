from src.agentic_ai.state.graph_state import GraphState
from src.agentic_ai.models.groqllm import GroqLLM


class BasicChatbotNode:
    def __init__(self, model):
        self.model = model

    def process(self, state: GraphState):
            """
            Process the chatbot node.
            """
            
            return {
                "messages": self.model.invoke(state["messages"])
            }