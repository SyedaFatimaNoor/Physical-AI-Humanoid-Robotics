import os
from openai import OpenAI
from .db import qdrant_client

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

COLLECTION_NAME = "textbook_chunks"

def get_embedding(text: str):
    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    return response.data[0].embedding

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
        {"role": "system", "content": "You are an expert AI assistant for a Physical AI & Humanoid Robotics textbook. Use the provided context to answer the user's question. If the answer is not in the context, use your general knowledge but mention that it's outside the textbook scope."},
        {"role": "user", "content": f"Context:\n{context_str}\n\nQuestion: {query}"}
    ]
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )
    return response.choices[0].message.content
