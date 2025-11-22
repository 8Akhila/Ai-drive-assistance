"""
FAISS Vector Store

Stores:
✔ Embeddings
✔ Metadata: filename, snippet, google drive link

Supports:
✔ Batch insert (Windows friendly)
✔ Persistent saving between sessions
"""

import os
import faiss
import numpy as np
import json

VECTOR_DIM = 384  # must match embedding model dimension

# Storage paths
INDEX_PATH = "backend/app/data/faiss_index.bin"
META_PATH = "backend/app/data/faiss_meta.json"


class FaissStore:

    def __init__(self, dim: int = VECTOR_DIM):

        self.dim = dim

        # Load or create FAISS index
        if os.path.exists(INDEX_PATH):
            self.index = faiss.read_index(INDEX_PATH)
        else:
            self.index = faiss.IndexFlatL2(self.dim)

        # Load metadata list
        if os.path.exists(META_PATH):
            with open(META_PATH, "r", encoding="utf-8") as f:
                self.meta = json.load(f)
        else:
            self.meta = []

    def save(self):
        """Writes index + metadata to disk."""
        print(f"💾 Saving FAISS index → {INDEX_PATH}")
        print(f"💾 Saving metadata → {META_PATH}")

        faiss.write_index(self.index, INDEX_PATH)

        with open(META_PATH, "w", encoding="utf-8") as f:
            json.dump(self.meta, f, indent=2)

        print("✅ Save complete")

    def add(self, vector: np.ndarray, metadata: dict):
        """Inserts a single embedding."""
        if vector.ndim == 1:
            vector = np.expand_dims(vector, axis=0)

        self.index.add(vector.astype("float32"))
        self.meta.append(metadata)
        self.save()

    def add_batch(self, vectors, metadata_list):
        """Batch insert (FAST + Windows-safe)."""
        vectors = np.asarray(vectors, dtype="float32")
        self.index.add(vectors)

        self.meta.extend(metadata_list)

        self.save()

    def search(self, vector: np.ndarray, k: int = 5):
        """Retrieves closest matches."""
        if vector.ndim == 1:
            vector = np.expand_dims(vector, axis=0)

        distances, ids = self.index.search(vector.astype("float32"), k)

        return [
            self.meta[idx] for idx in ids[0] if 0 <= idx < len(self.meta)
        ]
