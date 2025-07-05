import os
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from .search_tool import search_news

news_analyst = LlmAgent(
    name="news_analyst",
    model=LiteLlm(
        model="openai/gpt-4o-mini",
        api_key=os.getenv("OPENAI_API_KEY"),
    ),
    description="News analyst agent",
    instruction="""
    You are a helpful assistant that can analyze news articles and provide a summary of the news.

    When asked about news, you should use the google_search tool to search for the news.

    If the user ask for news using a relative time, you should use the get_current_time tool to get the current time to use in the search query.
    """,
    tools=[search_news],
)
