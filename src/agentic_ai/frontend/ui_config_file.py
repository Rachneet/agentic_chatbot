from configparser import ConfigParser


class UIConfig:
    def __init__(self, config_file='src/agentic_ai/frontend/ui_config.ini'):
        self.config = ConfigParser()
        self.config.read(config_file)

    def get_llm_options(self):
        return self.config.get('DEFAULT', 'LLM_OPTIONS', fallback=['Groq']).split(', ')

    def get_usecase_options(self):
        return self.config.get('DEFAULT', 'USECASE_OPTIONS', fallback=['Basic Chatbot']).split(', ')

    def get_groq_model_options(self):
        return self.config.get('DEFAULT', 'GROQ_MODEL_OPTIONS', fallback=['llama-3.1-8b-instant']).split(', ')
    
    def get_page_title(self):
        return self.config.get('DEFAULT', 'PAGE_TITLE', fallback='LangGraph: Stateful Agentic AI Chatbot')


if __name__ == "__main__":
    config = UIConfig()
    print("Page Title:", config.get_page_title())
    print("LLM Options:", config.get_llm_options())
    print("Usecase Options:", config.get_usecase_options())
    print("Groq Model Options:", config.get_groq_model_options())
