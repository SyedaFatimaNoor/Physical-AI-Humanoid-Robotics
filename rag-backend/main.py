# main.py
"""FastAPI entrypoint for the Physical AI textbook RAG backend.

Deployed on Vercel Serverless (Python runtime). Vercel expects a `api` directory with a handler function.
Here we expose `/api/chat` and `/api/translate` endpoints.
"""

from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv
import os
load_dotenv()
from rag import get_answer
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    query: str
    selected_text: str | None = None
    user_id: str | None = None

class TranslateRequest(BaseModel):
    chapter: str
    language: str = "ur"
    user_id: str | None = None

@app.post("/api/chat")
async def chat_endpoint(req: ChatRequest):
    # Authentication placeholder – Vercel will forward JWT in headers
    # In production, verify JWT via Better Auth SDK
    answer = await get_answer(req.query, req.selected_text)
    return JSONResponse(content={"answer": answer})

@app.post("/api/translate")
async def translate_endpoint(req: TranslateRequest):
    # Simple wrapper – actual translation logic in rag.py
    translated = await get_answer(f"Translate the following to {req.language}: {req.chapter}")
    return JSONResponse(content={"translated": translated})

# New personalize endpoint
@app.post("/api/personalize")
async def personalize_endpoint(req: dict):
    """Expect JSON with 'text' and optional 'level' to personalize content."""
    text = req.get("text")
    level = req.get("level", "beginner")
    if not text:
        raise HTTPException(status_code=400, detail="Missing 'text' field")
    prompt = f"Personalize the following content for a {level} learner. Use markdown and keep tone friendly.\n\n{text}"
    personalized = await get_answer(prompt)
    return JSONResponse(content={"personalized_markdown": personalized})

class SignInRequest(BaseModel):
    email: str
    password: str

# Authentication endpoints using Better Auth
from auth import User, create_user, authenticate_user

@app.post("/api/signup")
async def signup(user: User):
    user_id = await create_user(user)
    if not user_id:
        raise HTTPException(status_code=400, detail="User creation failed")
    return {"user_id": user_id}

@app.post("/api/signin")
async def signin(req: SignInRequest):
    user = await authenticate_user(req.email, req.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"user": user}
