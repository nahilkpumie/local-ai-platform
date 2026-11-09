"""Fonctions partagées : connexion à LiteLLM et à la base vectorielle Chroma."""
import os
from pathlib import Path

import chromadb
from dotenv import load_dotenv
from openai import OpenAI

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env", override=True)

EMBED_MODEL = "local-embed"
CHAT_MODEL = os.getenv("RAG_CHAT_MODEL", "gemini-flash")
COLLECTION = "docs"


def llm_client() -> OpenAI:
    """Client OpenAI pointé vers LiteLLM (et non vers OpenAI)."""
    return OpenAI(
        base_url="http://localhost:4000/v1",
        api_key=os.environ["RAG_LITELLM_KEY"],
    )


def collection():
    """Base vectorielle stockée sur disque dans rag/.chroma/."""
    db = chromadb.PersistentClient(path=str(ROOT / "rag" / ".chroma"))
    return db.get_or_create_collection(COLLECTION, metadata={"hnsw:space": "cosine"})


def embed(client: OpenAI, texts: list[str]) -> list[list[float]]:
    """Transforme des textes en vecteurs via le modèle d'embedding local."""
    response = client.embeddings.create(model=EMBED_MODEL, input=texts)
    return [item.embedding for item in response.data]
