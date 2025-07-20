from dotenv import load_dotenv
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from manager.agent import root_agent
from typing import Optional

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Multi-Agent System API",
    description="API for interacting with the multi-agent system",
    version="1.0.0"
)

# Initialize session service
session_service = InMemorySessionService()

# Initialize the runner with the manager agent
runner = Runner(
    agent=root_agent,
    app_name="Multi-Agent System",
    session_service=session_service,
)

class ChatRequest(BaseModel):
    message: str
    user_id: str = "default_user"
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: Optional[str]
    session_id: str

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # Create or get session
        if not request.session_id:
            session = session_service.create_session(
                app_name="Multi-Agent System",
                user_id=request.user_id
            )
            session_id = session.id
        else:
            session_id = request.session_id

        # Create message content
        content = types.Content(
            role="user",
            parts=[types.Part(text=request.message)]
        )

        # Process message through agent
        response = None
        for event in runner.run(
            user_id=request.user_id,
            session_id=session_id,
            new_message=content
        ):
            if event.is_final_response() and event.content and event.content.parts:
                response = event.content.parts[0].text

        return ChatResponse(
            response=response,
            session_id=session_id
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8081)),
        reload=True  # Enable auto-reload for development
    ) 