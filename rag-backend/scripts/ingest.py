# ingest.py
"""Ingest generated markdown chapters into Qdrant and Neon.

1. Reads all `.md` files from `../textbook-frontend/docs/`.
2. Splits each file into chunks (≈500 tokens) using a simple newline splitter.
3. Generates embeddings via OpenAI `text-embedding-3-large`.
4. Upserts vectors into Qdrant collection `textbook_chunks`.
5. Stores metadata (chapter, source path) in Neon Postgres table `chapter_metadata`.
"""
import os
import glob
from pathlib import Path
import asyncio
import json

import openai
from qdrant_client import QdrantClient
import asyncpg

# Environment variables (set in Vercel or local dev)
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
NEON_DB_URL = os.getenv("NEON_DB_URL")

openai.api_key = OPENAI_API_KEY
qdrant = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
COLLECTION_NAME = "textbook_chunks"

async def _init_qdrant():
    # Create collection if it does not exist
    if COLLECTION_NAME not in [c.name for c in qdrant.get_collections().collections]:
        qdrant.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=qdrant_client.models.VectorParams(size=1536, distance="Cosine"),
        )

async def _embed_text(text: str):
    resp = await openai.embeddings.create(model="text-embedding-3-large", input=text)
    return resp.data[0].embedding

def _split_into_chunks(text: str, max_tokens: int = 500):
    # Very naive splitter: split on double newlines
    paragraphs = text.split("\n\n")
    chunks = []
    current = ""
    for p in paragraphs:
        if len((current + "\n\n" + p).split()) > max_tokens:
            chunks.append(current.strip())
            current = p
        else:
            current += "\n\n" + p
    if current:
        chunks.append(current.strip())
    return chunks

async def _upsert_chunks(chunks, chapter, source_path):
    vectors = []
    payloads = []
    for idx, chunk in enumerate(chunks):
        embed = await _embed_text(chunk)
        vectors.append(embed)
        payloads.append({"text": chunk, "chapter": chapter, "source": source_path, "chunk_id": idx})
    qdrant.upsert(
        collection_name=COLLECTION_NAME,
        points=[
            qdrant_client.models.PointStruct(id=f"{chapter}_{idx}", vector=v, payload=p)
            for idx, (v, p) in enumerate(zip(vectors, payloads))
        ],
    )

async def _store_metadata(chapter, source_path, num_chunks):
    pool = await asyncpg.create_pool(NEON_DB_URL)
    async with pool.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO chapter_metadata (chapter, source_path, chunk_count)
            VALUES ($1, $2, $3)
            ON CONFLICT (chapter) DO UPDATE SET source_path = EXCLUDED.source_path, chunk_count = EXCLUDED.chunk_count;
            """,
            chapter,
            source_path,
            num_chunks,
        )
    await pool.close()

async def main():
    await _init_qdrant()
    docs_path = Path(__file__).resolve().parents[2] / "textbook-frontend" / "docs"
    md_files = glob.glob(str(docs_path / "*.md"))
    for md_file in md_files:
        chapter = Path(md_file).stem
        with open(md_file, "r", encoding="utf-8") as f:
            content = f.read()
        chunks = _split_into_chunks(content)
        await _upsert_chunks(chunks, chapter, md_file)
        await _store_metadata(chapter, md_file, len(chunks))
        print(f"Ingested {chapter}: {len(chunks)} chunks")

if __name__ == "__main__":
    asyncio.run(main())
