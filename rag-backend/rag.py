# rag.py
"""Core Retrieval-Augmented Generation logic with pluggable LLM providers."""
import asyncio
import os
from typing import Awaitable, Callable, List, Tuple

from dotenv import load_dotenv
from qdrant_client import QdrantClient

# Load environment variables from .env if present
load_dotenv()

COLLECTION_NAME = "textbook_chunks"

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openrouter").lower()

if not QDRANT_URL or not QDRANT_API_KEY:
    raise RuntimeError("QDRANT_URL and QDRANT_API_KEY must be set.")

qdrant = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

EmbedFn = Callable[[str], Awaitable[List[float]]]
GenerateFn = Callable[[str], Awaitable[str]]


def _require_env(var_name: str) -> str:
    value = os.getenv(var_name)
    if not value:
        raise RuntimeError(f"{var_name} must be set when using provider '{LLM_PROVIDER}'.")
    return value


async def _gemini_embed(text: str) -> List[float]:
    import google.generativeai as genai  # lazy import to avoid dependency unless needed

    def _embed():
        resp = genai.embed_content(model=GEMINI_EMBED_MODEL, content=text)
        return resp["embedding"]

    return await asyncio.to_thread(_embed)


async def _gemini_generate(prompt: str) -> str:
    import google.generativeai as genai

    def _generate():
        model = genai.GenerativeModel(GEMINI_MODEL)
        system_prompt = "You are an expert AI tutor for Physical AI & Humanoid Robotics. Provide clear, structured, and educational responses using markdown formatting. Focus on helping students learn effectively with practical examples and accessible explanations."
        
        full_prompt = f"{system_prompt}\n\n{prompt}"
        response = model.generate_content(
            [{"role": "user", "parts": [full_prompt]}],
            generation_config={
                "temperature": 0.3,
            },
        )
        return (response.text or "").strip()

    return await asyncio.to_thread(_generate)


async def _openrouter_embed(text: str) -> List[float]:
    resp = await OPENROUTER_CLIENT.embeddings.create(model=OPENROUTER_EMBED_MODEL, input=text)
    return resp.data[0].embedding


async def _openrouter_generate(prompt: str) -> str:
    completion = await OPENROUTER_CLIENT.chat.completions.create(
        model=OPENROUTER_MODEL,
        messages=[
            {
                "role": "system", 
                "content": "You are an expert AI tutor for Physical AI & Humanoid Robotics. Provide clear, structured, and educational responses using markdown formatting. Focus on helping students learn effectively with practical examples and accessible explanations."
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
    )
    return completion.choices[0].message.content.strip()


if LLM_PROVIDER == "gemini":
    import google.generativeai as genai

    GEMINI_API_KEY = _require_env("GEMINI_API_KEY")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    GEMINI_EMBED_MODEL = os.getenv("GEMINI_EMBED_MODEL", "text-embedding-004")

    genai.configure(api_key=GEMINI_API_KEY)
    embed_text: EmbedFn = _gemini_embed
    generate_text: GenerateFn = _gemini_generate
else:
    from openai import AsyncOpenAI

    OPENROUTER_API_KEY = _require_env("OPENROUTER_API_KEY")
    OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")
    OPENROUTER_EMBED_MODEL = os.getenv("OPENROUTER_EMBED_MODEL", "text-embedding-3-small")
    OPENROUTER_CLIENT = AsyncOpenAI(base_url="https://openrouter.ai/api/v1", api_key=OPENROUTER_API_KEY)

    embed_text = _openrouter_embed
    generate_text = _openrouter_generate


async def _search(query: str, top_k: int = 5) -> List[Tuple[str, str]]:
    """Search Qdrant for the most similar chunks. Returns a list of (chunk_id, text)."""
    query_vec = await embed_text(query)
    results = qdrant.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vec,
        limit=top_k,
        with_payload=True,
    )
    return [(hit.id, hit.payload["text"]) for hit in results]


async def get_answer(query: str, selected_text: str | None = None) -> str:
    """Generate an answer using retrieved context. Optionally scope to selected text."""
    context_chunks = await _search(query)
    context_text = "\n\n".join([c[1] for c in context_chunks])
    
    prompt = (
        "You are an expert AI tutor for the Physical AI & Humanoid Robotics textbook. "
        "Your goal is to provide clear, comprehensive, and educational responses that help students learn effectively.\n\n"
        "Guidelines for your responses:\n"
        "1. Use ONLY the provided textbook context to answer questions\n"
        "2. Structure your answers with clear headings and bullet points when appropriate\n"
        "3. Provide practical examples and real-world applications when possible\n"
        "4. Explain technical concepts in an accessible way for learners\n"
        "5. If the context doesn't contain enough information, clearly state the limitations\n"
        "6. Use markdown formatting for better readability (bold, lists, code blocks)\n"
        "7. Keep responses concise yet comprehensive (150-300 words typically)\n\n"
        f"Context from textbook:\n{context_text}\n\n"
        f"User Question: {query}\n"
    )
    
    if selected_text:
        prompt += (
            f"\nSelected Text for context:\n{selected_text}\n"
            "Please explain this specific passage in detail, connecting it to broader concepts from the textbook."
        )

    return await generate_text(prompt)
