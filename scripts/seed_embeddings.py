import os
import json
import chromadb
from openai import OpenAI
from dotenv import load_dotenv

# Load your OpenAI API key from .env file
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Setup Chroma client with local storage
chroma_client = chromadb.PersistentClient(path="./chroma_db")

# Create or get a collection to store embeddings
collection = chroma_client.get_or_create_collection(name="closr-store")

# Load data files
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "backend", "data")

def load_json(filename):
    with open(os.path.join(DATA_DIR, filename), "r") as f:
        return json.load(f)

products = load_json("products.json")
faqs = load_json("faqs.json")

# Combine all texts to embed (products + FAQs)
documents = []
metadatas = []
ids = []

# Add product entries
for i, prod in enumerate(products):
    text = f"Product: {prod['title']} - {prod['description']}"
    documents.append(text)
    metadatas.append({"type": "product", "id": prod["id"]})
    ids.append(f"product_{i}")

# Add FAQ entries
for i, faq in enumerate(faqs):
    text = f"FAQ: {faq['question']} - {faq['answer']}"
    documents.append(text)
    metadatas.append({"type": "faq"})
    ids.append(f"faq_{i}")

# Embed using OpenAI API
def get_embeddings(texts):
    from openai import OpenAI

    client = OpenAI(api_key=openai_api_key)

    def get_embeddings(texts):
        response = client.embeddings.create(
            input=texts,
            model="text-embedding-3-small"
        )
        return [r.embedding for r in response.data]

print("Generating embeddings...")
embeddings = get_embeddings(documents)

# Save to Chroma
collection.add(documents=documents, metadatas=metadatas, ids=ids, embeddings=embeddings)
print("✅ Embeddings stored in Chroma DB!")
