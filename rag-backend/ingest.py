import os
import glob
from pathlib import Path
from typing import List, Dict
import google.generativeai as genai
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import hashlib

# Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
COLLECTION_NAME = "textbook_chunks"
DOCS_DIR = "../textbook-frontend/docs"

# Initialize clients
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

qdrant_client = None
if QDRANT_URL and QDRANT_API_KEY:
    qdrant_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

def get_embedding(text: str) -> List[float]:
    """Generate embedding for text using Gemini"""
    if not GEMINI_API_KEY:
        print("Warning: No Gemini API key, using mock embeddings")
        return [0.0] * 768
    
    result = genai.embed_content(
        model="models/text-embedding-004",
        content=text,
        task_type="retrieval_document",
        title="Textbook chunk"
    )
    return result['embedding']

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100) -> List[str]:
    """Split text into overlapping chunks"""
    words = text.split()
    chunks = []
    
    for i in range(0, len(words), chunk_size - overlap):
        chunk = ' '.join(words[i:i + chunk_size])
        if len(chunk.strip()) > 50:  # Minimum chunk size
            chunks.append(chunk)
    
    return chunks

def extract_metadata(filepath: str, content: str) -> Dict:
    """Extract metadata from markdown file"""
    filename = os.path.basename(filepath)
    
    # Extract chapter number and title
    if filename.startswith('chapter-'):
        parts = filename.replace('.md', '').split('-')
        chapter_num = parts[1] if len(parts) > 1 else '0'
        title = ' '.join(parts[2:]).title() if len(parts) > 2 else 'Unknown'
    elif filename == 'intro.md':
        chapter_num = '0'
        title = 'Introduction'
    else:
        chapter_num = '99'
        title = filename.replace('.md', '').replace('-', ' ').title()
    
    # Extract first heading as section
    lines = content.split('\n')
    section = 'General'
    for line in lines:
        if line.startswith('##'):
            section = line.replace('#', '').strip()
            break
    
    return {
        'filename': filename,
        'chapter': chapter_num,
        'title': title,
        'section': section,
        'filepath': filepath
    }

def process_markdown_file(filepath: str) -> List[Dict]:
    """Process a single markdown file into chunks with metadata"""
    print(f"Processing: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove frontmatter
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            content = parts[2]
    
    # Extract metadata
    metadata = extract_metadata(filepath, content)
    
    # Chunk the content
    chunks = chunk_text(content)
    
    # Create documents
    documents = []
    for i, chunk in enumerate(chunks):
        doc_id = hashlib.md5(f"{filepath}_{i}".encode()).hexdigest()
        documents.append({
            'id': doc_id,
            'text': chunk,
            'metadata': {
                **metadata,
                'chunk_index': i,
                'total_chunks': len(chunks)
            }
        })
    
    return documents

def create_collection():
    """Create or recreate Qdrant collection"""
    if not qdrant_client:
        print("Error: Qdrant client not initialized")
        return False
    
    try:
        # Delete existing collection
        try:
            qdrant_client.delete_collection(COLLECTION_NAME)
            print(f"Deleted existing collection: {COLLECTION_NAME}")
        except:
            pass
        
        # Create new collection
        qdrant_client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=768, distance=Distance.COSINE)
        )
        print(f"Created collection: {COLLECTION_NAME}")
        return True
    
    except Exception as e:
        print(f"Error creating collection: {e}")
        return False

def ingest_documents():
    """Main ingestion function"""
    print("=" * 60)
    print("Starting document ingestion...")
    print("=" * 60)
    
    # Find all markdown files
    docs_path = Path(DOCS_DIR)
    if not docs_path.exists():
        print(f"Error: Docs directory not found: {DOCS_DIR}")
        return
    
    md_files = list(docs_path.glob("*.md"))
    print(f"\nFound {len(md_files)} markdown files")
    
    # Process all files
    all_documents = []
    for filepath in md_files:
        docs = process_markdown_file(str(filepath))
        all_documents.extend(docs)
    
    print(f"\nTotal chunks created: {len(all_documents)}")
    
    # Create collection
    if not create_collection():
        return
    
    # Generate embeddings and upload
    print("\nGenerating embeddings and uploading to Qdrant...")
    points = []
    
    for i, doc in enumerate(all_documents):
        if i % 10 == 0:
            print(f"Processing {i}/{len(all_documents)}...")
        
        embedding = get_embedding(doc['text'])
        
        point = PointStruct(
            id=doc['id'],
            vector=embedding,
            payload={
                'text': doc['text'],
                **doc['metadata']
            }
        )
        points.append(point)
        
        # Upload in batches of 100
        if len(points) >= 100:
            qdrant_client.upsert(
                collection_name=COLLECTION_NAME,
                points=points
            )
            points = []
    
    # Upload remaining points
    if points:
        qdrant_client.upsert(
            collection_name=COLLECTION_NAME,
            points=points
        )
    
    print("\n" + "=" * 60)
    print("✅ Ingestion complete!")
    print(f"Total documents indexed: {len(all_documents)}")
    print("=" * 60)

if __name__ == "__main__":
    ingest_documents()
