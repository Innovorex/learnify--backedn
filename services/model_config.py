import os
from dotenv import load_dotenv

load_dotenv()

# Garuda AI Configuration (Primary for AI Tutor)
GARUDA_API_KEY = os.getenv("GARUDA_API_KEY")
GARUDA_BASE_URL = os.getenv("GARUDA_BASE_URL", "https://devai.innovorex.co.in/api/v1")
GARUDA_MODEL = os.getenv("GARUDA_MODEL", "llama3.2:3b")

# OpenRouter Configuration (Used for Question Generation & Fallback for AI Tutor)
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3.3-8b-instruct:free")

# AI Tutor Fallback Model (OpenRouter)
AI_TUTOR_FALLBACK_MODEL = os.getenv("AI_TUTOR_FALLBACK_MODEL", "anthropic/claude-3.5-haiku")

# RAG Configuration
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "./chroma_db")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "ignou_pedagogy")

# IGNOU Content Path
IGNOU_CONTENT_PATH = "./ignou_pedagogy_content"

# Service Configuration
GARUDA_TIMEOUT = int(os.getenv("GARUDA_TIMEOUT", "30"))
OPENROUTER_TIMEOUT = int(os.getenv("OPENROUTER_TIMEOUT", "60"))

# Print configuration status
print(f"🔑 Garuda AI Key Loaded: {'✔️' if GARUDA_API_KEY else '❌'}")
if GARUDA_API_KEY:
    print(f"🔑 Garuda API Key (first 20 chars): {GARUDA_API_KEY[:20]}...")
    print(f"🤖 Garuda Model: {GARUDA_MODEL}")

print(f"🔑 OpenRouter Key Loaded: {'✔️' if OPENROUTER_API_KEY else '❌'}")
if OPENROUTER_API_KEY:
    print(f"🔑 OpenRouter API Key (first 20 chars): {OPENROUTER_API_KEY[:20]}...")
    print(f"🤖 OpenRouter Model: {OPENROUTER_MODEL}")
    print(f"🤖 AI Tutor Fallback Model: {AI_TUTOR_FALLBACK_MODEL}")
