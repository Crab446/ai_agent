import streamlit as st
from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.duckduckgo import DuckDuckGoTools
import os
from dotenv import load_dotenv

load_dotenv()

# os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["GROQ_API_KEY"] = st.secrets("GROQ_API_KEY")

agent = Agent(
    model=Groq(id="qwen-2.5-32b"),
    description="You are an assistant, please reply based on the question",
    tools=[DuckDuckGoTools()],
    markdown=True
)

def main():
    st.title("AI Assistant")
    st.markdown("### Description")
    st.write("This AI assistant can help answer your questions and provide information.")

    if 'queries' not in st.session_state:
        st.session_state.queries = []

    # Input field for user query
    user_query = st.text_input("Ask me anything:")

    # Button to submit the query
    if st.button("Submit"):
        if user_query:
            st.session_state.queries.append(user_query)
            with st.spinner("Processing..."):
                # Get the response from the AI agent
                response = agent.run(user_query)
                # Extract the content from the response
                answer = response.content
            # Display the answer
            st.markdown("### Response:")
            st.write(answer)
        else:
            st.warning("Please enter a question.")

    # Display conversation history
    st.markdown("### Conversation History:")
    for i, query in enumerate(st.session_state.queries):
        st.write(f"**User**: {query}")
        if i < len(st.session_state.queries) - 1:
            response = agent.run(query)
            answer = response.content
            st.write(f"**Assistant**: {answer}")

if __name__ == "__main__":
    main()
