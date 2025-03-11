import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from query import ObsidianRAG
from ingest import ingest_obsidian_vault

app = FastAPI(title="Obsidian RAG API")
rag = None  # Will be initialized on startup

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str
    sources: List[str]

class SearchRequest(BaseModel):
    query: str
    k: Optional[int] = 5

@app.on_event("startup")
async def startup_event():
    global rag
    # Initialize the RAG system
    rag = ObsidianRAG()

@app.post("/query", response_model=QueryResponse)
async def query_rag(request: QueryRequest):
    if not rag:
        raise HTTPException(status_code=503, detail="RAG system not initialized")
    
    result = rag.query(request.question)
    return result

@app.post("/search", response_model=List[Dict[str, Any]])
async def similarity_search(request: SearchRequest):
    if not rag:
        raise HTTPException(status_code=503, detail="RAG system not initialized")
    
    results = rag.similarity_search(request.query, k=request.k)
    return results

@app.post("/ingest")
async def ingest_vault():
    try:
        ingest_obsidian_vault()
        return {"status": "success", "message": "Vault ingested successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)