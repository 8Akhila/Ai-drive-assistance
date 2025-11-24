"""
===================================
📦 FAISS VECTOR STORE (Persistence)
===================================

Stores:
✔ Chunk embeddings (vector database)
✔ Metadata (filename, snippet, Drive link, detected IDs)

Supports:
✔ Persistent storage (index + metadata)
✔ Batch insert optimized for Windows
✔ Top-K similarity search
✔ Direct metadata ID lookup (PAN/Aadhaar)
"""

import os
import faiss
import numpy as np
import json

VECTOR_DIM = 384  # must match your embedding model

INDEX_PATH = "backend/app/data/faiss_index.bin"
META_PATH = "backend/app/data/faiss_meta.json"


class FaissStore:

    def __init__(self, dim: int = VECTOR_DIM):
        self.dim = dim

        # Load or create index
        if os.path.exists(INDEX_PATH):
            print("📂 Loading FAISS index...")
            self.index = faiss.read_index(INDEX_PATH)
        else:
            print("🆕 Creating new FAISS index...")
            self.index = faiss.IndexFlatL2(self.dim)

        # Load metadata list
        if os.path.exists(META_PATH):
            print("📂 Loading metadata...")
            with open(META_PATH, "r", encoding="utf-8") as f:
                self.meta = json.load(f)
        else:
            print("🆕 Creating metadata store...")
            self.meta = []

    def save(self):
        """Save FAISS + metadata to disk."""
        print(f"💾 Saving → {INDEX_PATH}")
        faiss.write_index(self.index, INDEX_PATH)

        with open(META_PATH, "w", encoding="utf-8") as f:
            json.dump(self.meta, f, indent=2)

    def add(self, vector: np.ndarray, metadata: dict):
        """Insert a single document embedding + metadata."""
        if vector.ndim == 1:
            vector = np.expand_dims(vector, axis=0)

        self.index.add(vector.astype("float32"))
        self.meta.append(metadata)
        self.save()

    def add_batch(self, vectors, metadata_list):
        """Insert multiple vectors and metadata at once."""
        vectors = np.asarray(vectors, dtype="float32")
        self.index.add(vectors)
        self.meta.extend(metadata_list)
        self.save()

    def search(self, vector: np.ndarray, k: int = 5):
        """Retrieve top-K closest stored embeddings."""
        if vector.ndim == 1:
            vector = np.expand_dims(vector, axis=0)

        distances, ids = self.index.search(vector.astype("float32"), k)

        return [
            self.meta[idx] for idx in ids[0]
            if 0 <= idx < len(self.meta)
        ]

    def search_by_id_value(self, query: str, max_results: int = 5):
        """
        🔍 NEW: Exact match search for Aadhaar, PAN, or specific extracted phrases.
        This is metadata-only search (no embeddings needed).
        """
        results = []

        query_upper = query.upper()

        for item in self.meta:
            snippet = item.get("snippet", "").upper()

            # match substring inside metadata text
            if query_upper in snippet:
                results.append(item)

            if len(results) >= max_results:
                break

        return results
            