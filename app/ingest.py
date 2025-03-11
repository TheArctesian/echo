import os
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from utils import load_obsidian_docs, split_docs

# Configuration
VAULT_PATH = "/data/obsidian_vault"
VECTOR_DB_PATH = "/storage/vector_db"
EMBEDDING_MODEL = "nomic-embed-text"

def ingest_obsidian_vault():
    """Process Obsidian vault and create vector database"""
    print(f"Loading documents from {VAULT_PATH}...")
    documents = load_obsidian_docs(VAULT_PATH)
    print(f"Loaded {len(documents)} documents")
    
    print("Splitting documents into chunks...")
    chunks = split_docs(documents)
    print(f"Created {len(chunks)} chunks")
    
    print(f"Initializing embeddings with model: {EMBEDDING_MODEL}")
    embeddings = OllamaEmbeddings(
        model=EMBEDDING_MODEL,
        base_url=os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
    )
    
    print(f"Creating vector database at {VECTOR_DB_PATH}...")
    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=VECTOR_DB_PATH
    )
    
    print(f"Vector database created with {len(chunks)} document chunks")
    print(f"Database persisted to {VECTOR_DB_PATH}")

if __name__ == "__main__":
    ingest_obsidian_vault()