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

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    tone = TONE_PROFILES.get(request.tone, TONE_PROFILES.get("Minimalist"))

    # Mocked context chunks for now (later will come from rag.py)
    mock_context = [
        "Product: Organic Cotton Hoodie - Soft, breathable, eco-friendly.",
        "FAQ: We offer a 14-day hassle-free return policy."
    ]

    # Use the prompt builder to create a final prompt
    prompt = build_prompt(
        message=request.message,
        tone=tone,
        context_chunks=mock_context
    )

    # For now, return the built prompt directly as the reply
    return ChatResponse(reply=prompt)