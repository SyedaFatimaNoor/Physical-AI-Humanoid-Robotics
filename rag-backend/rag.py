import os
from dotenv import load_dotenv
load_dotenv()

import httpx
from db import qdrant_client

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# Default model - you can change this to any model available on OpenRouter
# Popular options: "google/gemini-flash-1.5", "openai/gpt-4o-mini", "anthropic/claude-3-haiku"
DEFAULT_MODEL = os.getenv("OPENROUTER_MODEL", "google/gemini-flash-1.5")
EMBEDDING_MODEL = os.getenv("OPENROUTER_EMBEDDING_MODEL", "openai/text-embedding-3-small")

COLLECTION_NAME = "textbook_chunks"

def call_openrouter(messages: list, model: str = None) -> str:
    """Make a chat completion request to OpenRouter API."""
    if not OPENROUTER_API_KEY:
        return "OpenRouter API Key not found. Please set OPENROUTER_API_KEY in .env."
    
    model = model or DEFAULT_MODEL
    
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://physical-ai-textbook.com",
        "X-Title": "Physical AI Textbook RAG"
    }
    
    payload = {
        "model": model,
        "messages": messages
    }
    
    try:
        with httpx.Client(timeout=60.0) as client:
            response = client.post(
                f"{OPENROUTER_BASE_URL}/chat/completions",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
    except httpx.HTTPStatusError as e:
        return f"OpenRouter API error: {e.response.status_code} - {e.response.text}"
    except Exception as e:
        return f"Error calling OpenRouter: {str(e)}"

def get_embedding(text: str):
    """Get embeddings using OpenRouter's embedding endpoint."""
    if not OPENROUTER_API_KEY:
        return [0.0] * 1536  # Mock embedding if no key (1536 for OpenAI embeddings)
    
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://physical-ai-textbook.com",
        "X-Title": "Physical AI Textbook RAG"
    }
    
    payload = {
        "model": EMBEDDING_MODEL,
        "input": text
    }
    
    try:
        with httpx.Client(timeout=30.0) as client:
            response = client.post(
                f"{OPENROUTER_BASE_URL}/embeddings",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            data = response.json()
            return data["data"][0]["embedding"]
    except Exception as e:
        print(f"Embedding error: {e}")
        return [0.0] * 1536

def search_context(query: str, limit: int = 5):
    if not qdrant_client:
        return []
    
    query_vector = get_embedding(query)
    hits = qdrant_client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=limit
    )
    return [hit.payload for hit in hits]

def generate_answer(query: str, context: list):
    context_str = "\n\n".join([c.get('text', '') for c in context])
    
    messages = [
        {
            "role": "system",
            "content": """You are an expert AI assistant for a Physical AI & Humanoid Robotics textbook. 
Use the provided context to answer the user's question. 
If the answer is not in the context, use your general knowledge but mention that it's outside the textbook scope."""
        },
        {
            "role": "user",
            "content": f"""Context:
{context_str}

Question: {query}"""
        }
    ]
    
    return call_openrouter(messages)

def personalize_text(text: str, level: str):
    messages = [
        {
            "role": "system",
            "content": """You are an expert at adapting educational content for different skill levels.
            
Level Definitions:
- Beginner: Simple language, more analogies, define technical terms.
- Intermediate: Standard technical textbook style.
- Expert: Concise, focus on advanced concepts, assume prior knowledge."""
        },
        {
            "role": "user",
            "content": f"""Rewrite the following textbook content for a {level} level audience.

Content:
{text}"""
        }
    ]
    
    return call_openrouter(messages)

def translate_text(text: str, target_language: str):
    messages = [
        {
            "role": "system",
            "content": "You are an expert translator. Maintain markdown formatting exactly when translating."
        },
        {
            "role": "user",
            "content": f"""Translate the following textbook content into {target_language}.

Content:
{text}"""
        }
    ]
    
    return call_openrouter(messages)
