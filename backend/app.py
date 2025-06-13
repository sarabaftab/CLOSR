from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# Request schema
class ChatRequest(BaseModel):
    message: str
    tone: Optional[str] = "default"

# Response schema
class ChatResponse(BaseModel):
    reply: str

@app.get("/")
def read_root():
    return {"message": "CLOSR backend is running 🚀"}

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    # Placeholder response (we’ll add GPT + RAG logic later)
    dummy_reply = f"[Tone: {request.tone}] You said: '{request.message}'"
    return ChatResponse(reply=dummy_reply)

# To run: `uvicorn app:app --reload` (inside backend folder)
# This sets up our local API server.
