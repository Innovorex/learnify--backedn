import os
from dotenv import load_dotenv

load_dotenv()

# Model Configuration
AI_TUTOR_MODEL = os.getenv("AI_TUTOR_MODEL", "anthropic/claude-3.5-haiku")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# RAG Configuration
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "./chroma_db")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "ignou_pedagogy")

# IGNOU Content Path
IGNOU_CONTENT_PATH = "./ignou_pedagogy_content"

print(f"🔑 OpenRouter Key Loaded: {'✔️' if OPENROUTER_API_KEY else '❌'}")
if OPENROUTER_API_KEY:
    print(f"🔑 Using API Key (first 20 chars): {OPENROUTER_API_KEY[:20]}...")
