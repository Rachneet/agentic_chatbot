import json
import streamlit as st

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage


class DisplayStreamlitResult:

    def __init__(self, use_case, graph, user_message):
        self.use_case = use_case
        self.graph = graph
        self.user_message = user_message

    def display_result(self):
        """
        Display the result in a Streamlit app.
        """

        if self.use_case == "Basic Chatbot":
            for event in self.graph.stream({"messages": ("user", self.user_message)}):
                print(event.values())
                for value in event.values():
                    print(value["messages"])
                    with st.chat_message("user"):
                        st.write(self.user_message)
                    with st.chat_message("assistant"):
                        st.write(value["messages"].content)

        elif self.use_case == "Chatbot with Tools":
            initial_state = {"messages": self.user_message}
            res = self.graph.invoke(initial_state)

            for message in res["messages"]:
                if isinstance(message, HumanMessage):
                    with st.chat_message("user"):
                        st.write(message.content)
                
                elif isinstance(message, ToolMessage):
                    with st.chat_message("ai"):
                        st.write("Tool call sent")
                        st.write(message.content)
                        st.write("Tool call response received")

                elif isinstance(message, AIMessage):
                    with st.chat_message("assistant"):
                        st.write(message.content)
