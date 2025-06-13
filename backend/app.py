from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Optional
import os
import json
from chatbot.prompt_builder import build_prompt

app = FastAPI()

# Request schema
class ChatRequest(BaseModel):
    message: str
    tone: Optional[str] = "default"

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

from chatbot.rag import query_context  # Add this at the top with your imports

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    tone = TONE_PROFILES.get(request.tone, TONE_PROFILES.get("Minimalist"))

    # Retrieve relevant context from vector DB
    real_context = query_context(request.message)

    # Build final prompt using real context
    prompt = build_prompt(
        message=request.message,
        tone=tone,
        context_chunks=real_context
    )

    from openai import OpenAI  # Add to your imports at top
    openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # reuse env-loaded key

    response = openai_client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful and persuasive AI salesperson."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
    )

    reply = response.choices[0].message.content.strip()
    return ChatResponse(reply=reply)

