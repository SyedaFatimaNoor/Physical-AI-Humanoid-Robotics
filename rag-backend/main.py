from fastapi import FastAPI, HTTPException, UploadFile, File, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Physical AI RAG Backend")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from pydantic import BaseModel
from typing import List, Optional
from rag import search_context, generate_answer, get_embedding, personalize_text, translate_text
from db import init_db, get_db_connection

# Models
class ChatRequest(BaseModel):
    query: str
    history: Optional[List[dict]] = []

class PersonalizeRequest(BaseModel):
    text: str
    level: str # beginner, intermediate, expert

class TranslateRequest(BaseModel):
    text: str
    target_language: str = "Urdu"

@app.on_event("startup")
async def startup_event():
    init_db()

@app.post("/rag/ask")
async def ask_question(request: ChatRequest):
    context = search_context(request.query)
    answer = generate_answer(request.query, context)
    return {"answer": answer, "context": context}

class SelectionRequest(BaseModel):
    query: str
    selected_text: str

@app.post("/rag/ask-selection")
async def ask_selection(request: SelectionRequest):
    # For selection, we prioritize the selected text as context
    # We could also embed it to find related concepts, but direct usage is often best for "explain this"
    context = [{"text": request.selected_text, "source": "User Selection"}]
    answer = generate_answer(request.query, context)
    return {"answer": answer, "context": context}

@app.post("/rag/personalize")
async def personalize_content(request: PersonalizeRequest):
    personalized_text = personalize_text(request.text, request.level)
    return {
        "personalized_markdown": personalized_text,
        "meta": {"level": request.level}
    }

@app.post("/rag/translate")
async def translate_content(request: TranslateRequest):
    translated_text = translate_text(request.text, request.target_language)
    return {
        "translated_markdown": translated_text
    }

from auth import create_user, authenticate_user, User

class SignupRequest(User):
    pass

class SigninRequest(BaseModel):
    email: str
    password: str

@app.post("/auth/signup")
async def signup(user: SignupRequest):
    user_id = create_user(user)
    if user_id:
        return {"message": "User created successfully", "user_id": user_id}
    raise HTTPException(status_code=400, detail="User creation failed")

@app.post("/auth/signin")
async def signin(creds: SigninRequest):
    user = authenticate_user(creds.email, creds.password)
    if user:
        return {"message": "Login successful", "user": {"email": user['email'], "name": user['full_name']}}
    raise HTTPException(status_code=401, detail="Invalid credentials")


