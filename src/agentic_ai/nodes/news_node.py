from langchain_tavily import TavilySearch
from langchain_core.prompts import ChatPromptTemplate


class NewsNode:
    def __init__(self, model):
        """
        Initialize the NewsNode with a language model and a search tool.
        """
        self.model = model
        self.search_tool = TavilySearch(max_results=2)

        # capture the state of the node so that it can be shown at a later time
        self.state: dict = {}

    def fetch_news(self, state: dict) -> dict:
        """
        Fetch news articles and update the state with the results.

        Args:
            state (dict): The current state containing user messages and frequency.
        Returns:
            dict: Updated state with fetched news articles in `news_results` key.
        """
        
        frequency = state["messages"][0].content.lower()
        self.state["frequency"] = frequency

        time_range_map = {
            "past day": "day",
            "past week": "week",
            "past month": "month",
            "past year": "year",
        }
        days_map = {
            "past day": 1,
            "past week": 7,
            "past month": 30,
            "past year": 365,
        }

        response = TavilySearch(
            max_results=5,
            topic="news",
            include_answer="advanced",
            time_range=time_range_map.get(frequency, "day"),
            days=days_map.get(frequency, 1)
        )

        search_response = response.invoke({"query": "Latest AI News."})
        # print("Tavily response:", search_response)

        state["news_results"] = search_response.get("results", [])
        self.state["news_results"] = state["news_results"]
        return state
    
    def summarize_news(self, state: dict) -> dict:
        """
        Summarize the fetched news articles and update the state with the summary.

        Args:
            state (dict): The current state containing fetched news articles.
        Returns:
            dict: Updated state with summarized news articles in `news_summary` key.
        """

        news_results = self.state.get("news_results", [])
        if not news_results:
            return state    
        
        # extract data from news results from tavily
        articles_content = "\n\n".join(
            [
                f"Content: {article.get('content', '')} \n URL: {article.get('url', '')} \n Date: {article.get('published_date', '')}" 
                for article in news_results
            ]
        )

        system_message = """
        You are a helpful assistant that summarizes news articles.
        Summarize articles in a markdown format. For each article include:
        - Date in YYYY-MM-DD format
        - Summary of the article
        - Source URL

        Use the following format for each article:
        ### Date: YYYY-MM-DD
        - Summary of the article.
        - [Source](URL)
        """

        prompt_template = ChatPromptTemplate.from_messages([
            ("system", system_message),
            ("user", "Summarize the following news articles:\n\n{articles}.")
        ])

        summary = self.model.invoke(prompt_template.format(articles=articles_content)).content  
        state["news_summary"] = summary
        self.state["news_summary"] = summary
        return self.state
    
    def save_results(self, state: dict) -> dict:
        """
        Save the summarized news results to a file.

        Args:
            state (dict): The current state containing summarized news articles.
        Returns:
            dict: Updated state with a confirmation message in `save_confirmation` key.
        """

        frequency = self.state.get("frequency", "N/A")
        news_summary = self.state.get("news_summary", "")

        filename = f"./news/news_summary_{frequency.replace(' ', '_')}.md"

        with open(filename, "w") as f:
            f.write(f"# News Summary - {frequency.title()}\n\n")
            f.write(news_summary)

        confirmation_message = f"News summary saved to {filename}"
        state["save_confirmation"] = confirmation_message
        self.state["save_confirmation"] = confirmation_message
        return self.state
