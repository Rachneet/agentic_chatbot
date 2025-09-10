import streamlit as st
import os

from src.agentic_ai.frontend.ui_config_file import UIConfig


class LoadStreamlitUI:
    def __init__(self):
        self.config = UIConfig()
        self.user_controls = {}
        self.page_title = self.config.get_page_title()
        self.llm_options = self.config.get_llm_options()
        self.usecase_options = self.config.get_usecase_options()
        self.groq_model_options = self.config.get_groq_model_options()

    def setup_page(self):
        """
        Set up the Streamlit page configuration and title.
        """
        st.set_page_config(page_title=self.page_title, layout="wide")
        st.title(self.page_title)

    def display_sidebar(self):
        """
        Display sidebar and store in session state.
        """      
        st.sidebar.title("Configuration")
        
        # Store directly in session state
        st.session_state["selected_llm"] = st.sidebar.selectbox(
            "Select LLM", 
            self.llm_options,
            key="llm_select"
        )
        st.session_state["selected_usecase"] = st.sidebar.selectbox(
            "Select Use Case", 
            self.usecase_options,
            key="usecase_select"
        )

        if st.session_state["selected_llm"] == "Groq":
            st.session_state["selected_groq_model"] = st.sidebar.selectbox(
                "Select Groq Model", 
                self.groq_model_options,
                key="groq_model_select"
            )
            st.session_state["GROQ_API_KEY"] = st.sidebar.text_input(
                "Enter Groq API Key", 
                type="password",
                key="groq_api_key"
            )
            
            if not st.session_state["GROQ_API_KEY"]:
                st.sidebar.warning("Please enter your Groq API Key to proceed.")
        else: 
            st.session_state["selected_groq_model"] = None
            st.session_state["GROQ_API_KEY"] = None

    def get_user_controls(self):
        """Get current user controls from session state."""
        return {
            "selected_llm": st.session_state.get("selected_llm"),
            "selected_usecase": st.session_state.get("selected_usecase"), 
            "selected_groq_model": st.session_state.get("selected_groq_model"),
            "GROQ_API_KEY": st.session_state.get("GROQ_API_KEY")
        }

    def run(self):
        self.setup_page()
        self.display_sidebar()
