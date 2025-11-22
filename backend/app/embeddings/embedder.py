"""
Embedding Model (Local Offline Embeddings)

Uses a downloaded model (MiniLM) stored locally so the system works offline.
Protects memory by limiting large text input.
"""

import os
import numpy as np
from sentence_transformers import SentenceTransformer

LOCAL_MODEL_PATH = "./local_model"   # directory where model is stored
MAX_CHARS = 2000  # prevents memory overload on huge text chunks


class EmbeddingModel:

    def __init__(self):
        """Loads local model and validates it exists."""
        if not os.path.exists(LOCAL_MODEL_PATH):
            raise FileNotFoundError(
                "❌ Local model NOT found! Run: python backend/download_model.py"
            )

        print(f"🔵 Loading local embedding model from: {LOCAL_MODEL_PATH}")
        self.model = SentenceTransformer(LOCAL_MODEL_PATH)

    def _prepare(self, text: str) -> str:
        """Sanitizes text and ensures size is safe."""
        text = text.strip()
        return text[:MAX_CHARS] if len(text) > MAX_CHARS else text

    def embed(self, text: str) -> np.ndarray:
        """Returns embedding for text."""
        safe_text = self._prepare(text)
        emb = self.model.encode(safe_text, convert_to_numpy=True)
        return emb.astype("float32")

    def embed_query(self, query: str) -> np.ndarray:
        """Embedding function specifically for user queries."""
        return self.embed(query)

    def embed_text(self, text: str) -> np.ndarray:
        """Alias kept for compatibility."""
        return self.embed(text)
