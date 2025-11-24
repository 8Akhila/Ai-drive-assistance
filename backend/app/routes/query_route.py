# backend/app/routes/query_route.py

from fastapi import APIRouter

from backend.app.models.schemas import QueryRequest, QueryResponse, ChunkResult
from backend.app.embeddings.embedder import EmbeddingModel
from backend.app.vectorstore.faiss_store import FaissStore
from backend.app.rag.prompt_builder import build_prompt
from backend.app.rag.llm_engine import run_llm

router = APIRouter(prefix="/query")

# Load once globally for performance
embedder = EmbeddingModel()
faiss_store = FaissStore()


# ------------------------------------------------------------------
# 🔍 Helper: Detect if query looks numeric (phone / PAN / Aadhaar etc.)
# ------------------------------------------------------------------
def is_numeric_heavy(text: str) -> bool:
    digits = sum(c.isdigit() for c in text)
    return digits >= 6  # threshold for ID-like query


# ------------------------------------------------------------------
# 📌 MAIN QUERY ENDPOINT (Hybrid: ID Search → Keyword → Semantic)
# ------------------------------------------------------------------
@router.post("/", response_model=QueryResponse)
def run_query(payload: QueryRequest):

    query = payload.query.strip()

    # -------------------- 0️⃣ SPECIAL CASE: ID / EXACT STRING MATCH --------------------
    # This part is what YOU requested to add.
    # If the query looks like an ID (Aadhaar, PAN, phone), return instantly.
    id_matches = faiss_store.search_by_id_value(query)
    if id_matches:
        formatted = [
            ChunkResult(
                file_name=r.get("file_name", ""),
                snippet=r.get("snippet", ""),
                file_id=r.get("file_id", ""),
                drive_link=r.get("drive_link", "")
            )
            for r in id_matches
        ]
        return QueryResponse(
            answer="🔍 Found matching ID-based documents.",
            results=formatted
        )

    # -------------------- 🔁 If query contains many numbers attempt keyword search --------------------
    keyword_results = []
    if is_numeric_heavy(query):
        keyword_results = faiss_store.search_keyword(query)

        if keyword_results:  # Return immediately if found
            formatted = [
                ChunkResult(
                    file_name=r.get("file_name", ""),
                    snippet=r.get("snippet", ""),
                    file_id=r.get("file_id", ""),
                    drive_link=r.get("drive_link", "")
                )
                for r in keyword_results
            ]
            return QueryResponse(
                answer="🔍 Found related numeric records.",
                results=formatted
            )


    # -------------------- 1️⃣ SEMANTIC VECTOR SEARCH (Understanding meaning, not exact words) --------------------
    query_vector = embedder.embed_query(query)
    semantic_results = faiss_store.search(query_vector, k=7)

    # If semantic gives nothing, fallback to keyword search:
    if not semantic_results:
        semantic_results = faiss_store.search_keyword(query)

    # -------------------- ❌ NOTHING FOUND --------------------
    if not semantic_results:
        return QueryResponse(answer="❓ No matching documents found.", results=[])


    # -------------------- 2️⃣ Build RAG prompt using best search results --------------------
    prompt = build_prompt(semantic_results, query)

    # -------------------- 3️⃣ Generate LLM Answer --------------------
    answer = run_llm(prompt)

    # -------------------- 4️⃣ Format Results --------------------
    formatted_results = [
        ChunkResult(
            file_name=r.get("file_name", ""),
            snippet=r.get("snippet", ""),
            file_id=r.get("file_id", ""),
            drive_link=r.get("drive_link", "")
        )
        for r in semantic_results
    ]

    return QueryResponse(answer=answer, results=formatted_results)



# ------------------------------------------------------------------
# 🧪 Debug Route → Show FAISS Vector Count
# ------------------------------------------------------------------
@router.get("/debug/index_count")
def debug_index_count():
    return {"faiss_vectors": faiss_store.index.ntotal}
