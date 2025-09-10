import os
import streamlit as st

from langchain_groq import ChatGroq


class GroqLLM:
    def __init__(self, user_controls):
        self.user_controls = user_controls

    def get_llm_model(self):
        """
        Initialize and return the Groq LLM model based on user controls.
        """

        try:
            groq_api_key = self.user_controls.get("GROQ_API_KEY")
            groq_model = self.user_controls.get("selected_groq_model")

            if not groq_api_key and os.environ.get("GROQ_API_KEY") is None:
                st.error("Groq API Key is required. Please enter it to proceed.")

            llm = ChatGroq(model=groq_model, api_key=groq_api_key)

        except Exception as e:
            raise ValueError(f"Error initializing Groq LLM: {e}")
        
        return llm