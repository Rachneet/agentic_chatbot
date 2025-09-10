import streamlit as st

from src.agentic_ai.frontend.streamlit_ui.load_ui import LoadStreamlitUI
from src.agentic_ai.models.groqllm import GroqLLM
from src.agentic_ai.graph.graph_builder import GraphBuilder
from src.agentic_ai.frontend.streamlit_ui.display_result import DisplayStreamlitResult


def load_app():
    """
    Main function to run the Streamlit UI.
    """
    ui = LoadStreamlitUI()
    user_input = ui.get_user_controls()
    ui.run()

    if not user_input:
        st.error("Please provide the necessary inputs to proceed.")
        return

    user_message = st.chat_input("Enter your message: ")

    if user_message:
        try:
            # configure the chatbot with user controls
            user_controls = ui.get_user_controls()
            chatbot = GroqLLM(user_controls=user_controls)
            llm_model = chatbot.get_llm_model()

            if not llm_model:
                st.error("Failed to initialize the LLM model. Please check your configuration.")
                return

            # use case handling can be added here
            use_case = user_controls.get("selected_usecase")
            if not use_case:
                st.error("Please select a use case from the sidebar.")
                return

            # graph builder
            graph_builder = GraphBuilder(model=llm_model)
            
            try:
                graph = graph_builder.setup_graph(use_case)
                DisplayStreamlitResult(
                    use_case,
                    graph,
                    user_message
                ).display_result()
            except Exception as e:
                st.error(f"An error occurred: {e}")

        except Exception as e:
            raise ValueError(f"Error in application: {e}")
