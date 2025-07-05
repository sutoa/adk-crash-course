import os
from google.adk.agents import Agent, LlmAgent
from google.adk.models.lite_llm import LiteLlm

root_agent = LlmAgent(
    name="greeting_agent",
    # https://ai.google.dev/gemini-api/docs/models
    model=LiteLlm(
        model="openai/gpt-4o-mini",
        api_key=os.getenv("OPENAI_API_KEY"),
    ),
    description="Greeting agent",
    instruction="""
    You are a helpful assistant that greets the user. 
    Ask for the user's name and greet them by name.
    """,
)
