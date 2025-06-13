from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Optional
import os
import json
from chatbot.prompt_builder import build_prompt
from collections import defaultdict
from chatbot.rag import query_context 
from openai import OpenAI
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


app = FastAPI()

# Store message history for each session
chat_sessions = defaultdict(list)

# Request schema
class ChatRequest(BaseModel):
    message: str
    tone: Optional[str] = "default"
    session_id: Optional[str] = "default_user"

# Response schema
class ChatResponse(BaseModel):
    reply: str

# Load mock data
BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")

def load_json(filename):
    with open(os.path.join(DATA_DIR, filename), "r") as f:
        return json.load(f)

PRODUCTS = load_json("products.json")
FAQS = load_json("faqs.json")
TONE_PROFILES = load_json("tone_profiles.json")

@app.get("/")
def read_root():
    return {"message": "CLOSR backend is running 🚀"}

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    tone = TONE_PROFILES.get(request.tone, TONE_PROFILES.get("Minimalist"))
    session_id = request.session_id

    # Use real context from Chroma DB
    real_context = query_context(request.message)

    # Build the final prompt
    prompt = build_prompt(
        message=request.message,
        tone=tone,
        context_chunks=real_context
    )

    # Add user message to chat session history
    chat_sessions[session_id].append({"role": "user", "content": prompt})

    # Construct full conversation (with system message)
    full_conversation = [{"role": "system", "content": "You are a helpful and persuasive AI salesperson."}]
    full_conversation += chat_sessions[session_id]

    # Call OpenAI
    response = openai_client.chat.completions.create(
        model="gpt-4",
        messages=full_conversation,
        temperature=0.7,
    )

    reply = response.choices[0].message.content.strip()

    # Add assistant response to chat session history
    chat_sessions[session_id].append({"role": "assistant", "content": reply})

    return ChatResponse(reply=reply)
