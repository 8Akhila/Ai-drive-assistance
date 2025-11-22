# backend/app/routes/query_route.py

from fastapi import APIRouter

from backend.app.models.schemas import QueryRequest, QueryResponse, ChunkResult
from backend.app.embeddings.embedder import EmbeddingModel
from backend.app.vectorstore.faiss_store import FaissStore
from backend.app.rag.prompt_builder import build_prompt
from backend.app.rag.llm_engine import run_llm

router = APIRouter(prefix="/query")

# Load once
embedder = EmbeddingModel()
faiss_store = FaissStore()

@router.post("/", response_model=QueryResponse)
def run_query(payload: QueryRequest):

    query = payload.query
    mode = payload.mode       # ← NEW

    # ---------------------------
    # 1. Embed user query
    # ---------------------------
    query_vec = embedder.embed_query(query)

    # ---------------------------
    # 2. Search FAISS (top 7)
    # ---------------------------
    results = faiss_store.search(query_vec, k=7)

    if len(results) == 0:
        return QueryResponse(answer="I don't know.", results=[])

    # ---------------------------
    # 3. Build prompt (default/summary)
    # ---------------------------
    prompt = build_prompt(results, query, mode=mode)

    # ---------------------------
    # 4. LLM answer
    # ---------------------------
    answer = run_llm(prompt)

    # ---------------------------
    # 5. Convert metadata to Pydantic
    # ---------------------------
    response_chunks = [ChunkResult(**chunk) for chunk in results]

    return QueryResponse(
        answer=answer,
        results=response_chunks
    )


# Debug → count vectors in FAISS
@router.get("/debug/index_count")
def debug_index_count():
    return {"faiss_vectors": faiss_store.index.ntotal}
