# backend/app/models/schemas.py

from pydantic import BaseModel
from typing import List

# ---------------------------
# INPUT: What user sends
# ---------------------------
class QueryRequest(BaseModel):
    query: str                # User question
    mode: str = "default"     # NEW → "default" or "summary"


# ---------------------------
# RESULT CHUNK FROM FAISS
# ---------------------------
class ChunkResult(BaseModel):
    file_name: str
    snippet: str
    file_id: str
    drive_link: str


# ---------------------------
# OUTPUT: What API returns
# ---------------------------
class QueryResponse(BaseModel):
    answer: str                      # LLM final answer
    results: List[ChunkResult]       # Exact chunks used
