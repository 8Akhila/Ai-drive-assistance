import faiss
import numpy as np
import os
from backend.app.config import settings


# -------------------------------------------------------------
#  LOAD OR CREATE FAISS INDEX
# -------------------------------------------------------------
def load_or_create_index(dim=384):
    """
    Loads existing FAISS index from disk OR creates a fresh one.

    - MiniLM-L6-v2 model produces 384-dim vectors.
    - IndexFlatL2 → simplest & fast L2 distance search.
    """

    index_path = settings.VECTOR_INDEX_PATH

    # If index file exists → load it
    if os.path.exists(index_path):
        index = faiss.read_index(index_path)
        return index

    # Otherwise create a new empty index
    index = faiss.IndexFlatL2(dim)
    return index


# -------------------------------------------------------------
#  SAVE INDEX TO DISK
# -------------------------------------------------------------
def save_index(index):
    """
    Saves FAISS index to disk.
    Ensures folder exists before saving.
    """
    index_path = settings.VECTOR_INDEX_PATH

    os.makedirs(os.path.dirname(index_path), exist_ok=True)
    faiss.write_index(index, index_path)


# -------------------------------------------------------------
#  ADD VECTORS TO INDEX
# -------------------------------------------------------------
def add_embeddings(index, embeddings: np.ndarray):
    """
    Adds embedding vectors (numpy array) to FAISS index.
    Must be float32.
    """

    vectors = np.asarray(embeddings, dtype="float32")
    index.add(vectors)


# -------------------------------------------------------------
#  IMPROVED SEARCH (STEP 7)
# -------------------------------------------------------------
def search_index(index, query_vec: np.ndarray, k: int = 5):
    """
    Improved FAISS search:

    ✔ Fetch top-20 matches instead of top-5
    ✔ Filter poor matches using distance threshold
    ✔ Sort remaining by similarity
    ✔ Return top-k best results

    WHY THIS WORKS:
    - FAISS distance: lower = more similar
    - MiniLM embedding distances usually 0.4–1.0 for strong matches
    - Threshold prevents irrelevant files (e.g., images, random docs)
    """

    # Ensure correct shape (1, 384)
    if query_vec.ndim == 1:
        query_vec = query_vec.reshape(1, -1)

    # Step 1: Search top 20 candidates
    distances, ids = index.search(query_vec, 20)

    distances = distances[0]
    ids = ids[0]

    # Pair up (id, distance)
    pairs = list(zip(ids, distances))

    # Step 2: filter weak matches using distance threshold
    THRESHOLD = 1.20    # lower = more strict, higher = more documents included

    filtered = [(idx, dist) for idx, dist in pairs if dist < THRESHOLD]

    # Step 3: sort by best similarity (lowest distance first)
    filtered = sorted(filtered, key=lambda x: x[1])

    # Step 4: take top-K final results
    filtered = filtered[:k]

    # Step 5: split into IDs and distances
    final_ids = [x[0] for x in filtered]
    final_dist = [x[1] for x in filtered]

    return final_ids, final_dist
