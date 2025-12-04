import os
import yaml
import glob
from qdrant_client import QdrantClient
from qdrant_client.http import models
from rag import get_embedding, COLLECTION_NAME, QDRANT_URL, QDRANT_API_KEY

SPEC_PATH = "../spec/course.yaml"
DOCS_DIR = "../textbook-frontend/docs"

def load_spec():
    with open(SPEC_PATH, "r") as f:
        return yaml.safe_load(f)

def ingest_docs():
    if not QDRANT_URL or not QDRANT_API_KEY:
        print("Qdrant credentials not found.")
        return

    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
    
    # Recreate collection
    client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE),
    )

    spec = load_spec()
    chapters = spec['course']['chapters']
    
    points = []
    idx = 0
    
    for chapter in chapters:
        slug = chapter['slug']
        # Find matching file
        # Assuming filename matches slug or is close
        # For simplicity, we search for slug in filename
        files = glob.glob(os.path.join(DOCS_DIR, f"*{slug}*.md"))
        if not files:
            print(f"Warning: No file found for chapter {slug}")
            continue
            
        file_path = files[0]
        print(f"Processing {file_path}...")
        
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Robust Chunking Strategy
        # 1. Split by headers (##)
        # 2. Then split by paragraphs
        # 3. Enforce max chunk size ~1000 chars with overlap
        
        sections = content.split("\n## ")
        for section in sections:
            if not section.strip():
                continue
            
            # Add back the header marker if it wasn't the first block
            text_block = "## " + section if not section.startswith("# ") else section
            
            # Further split large sections
            chunks = split_text_with_overlap(text_block, chunk_size=1000, overlap=150)
            
            for chunk in chunks:
                embedding = get_embedding(chunk)
                
                points.append(models.PointStruct(
                    id=idx,
                    vector=embedding,
                    payload={
                        "text": chunk, 
                        "source": os.path.basename(file_path),
                        "chapter_slug": slug,
                        "title": chapter['title']
                    }
                ))
                idx += 1
                
                if len(points) >= 50:
                    client.upsert(collection_name=COLLECTION_NAME, points=points)
                    points = []
                    print(f"Indexed {idx} chunks...")

    if points:
        client.upsert(collection_name=COLLECTION_NAME, points=points)
        print(f"Finished indexing. Total chunks: {idx}")

def split_text_with_overlap(text, chunk_size, overlap):
    if len(text) <= chunk_size:
        return [text]
    
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += (chunk_size - overlap)
    return chunks

if __name__ == "__main__":
    ingest_docs()
