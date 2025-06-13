from openai import OpenAI
import chromadb
from dotenv import load_dotenv
import os

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

# Connect to Chroma DB
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection("closr-store")

def query_context(user_query: str, top_k: int = 4) -> list:
    """
    Embed the user query, search Chroma DB, and return top matching chunks.
    """
    embedding = client.embeddings.create(
        input=[user_query],
        model="text-embedding-3-small"
    ).data[0].embedding

    results = collection.query(
        query_embeddings=[embedding],
        n_results=top_k
    )

    return results["documents"][0] if results and "documents" in results else []
