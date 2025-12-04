import os
import google.generativeai as genai
from db import qdrant_client

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

COLLECTION_NAME = "textbook_chunks"

def get_embedding(text: str):
    if not GEMINI_API_KEY:
        return [0.0] * 768 # Mock embedding if no key
    result = genai.embed_content(
        model="models/text-embedding-004",
        content=text,
        task_type="retrieval_document",
        title="Embedding of single string"
    )
    return result['embedding']

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
    if not GEMINI_API_KEY:
        return "Gemini API Key not found. Please set GEMINI_API_KEY in .env."

    context_str = "\n\n".join([c.get('text', '') for c in context])
    
    prompt = f"""You are an expert AI assistant for a Physical AI & Humanoid Robotics textbook. 
    Use the provided context to answer the user's question. 
    If the answer is not in the context, use your general knowledge but mention that it's outside the textbook scope.

    Context:
    {context_str}

    Question: {query}
    """
    
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    return response.text
