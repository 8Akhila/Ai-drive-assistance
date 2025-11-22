import numpy as np   # For vector math

def normalize_vector(vec: np.ndarray) -> np.ndarray:
    """
    Normalizes an embedding vector so that its length becomes 1.
    This improves search quality in many cases.
    """

    norm = np.linalg.norm(vec)    # Calculate vector magnitude
    if norm == 0:                 # Prevent division by zero
        return vec
    return vec / norm             # Return normalized vector


def reshape_vector(vec: np.ndarray) -> np.ndarray:
    """
    Ensures that the vector has shape (1, dim) instead of (dim,).
    FAISS requires 2D arrays for searching.
    """

    if len(vec.shape) == 1:
        vec = vec.reshape(1, -1)   # Convert from (768,) → (1, 768)
    return vec                     # Return reshaped vector
