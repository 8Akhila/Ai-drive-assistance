from backend.app.config import settings   # Correct import path

def chunk_text(text: str) -> list[str]:
    """
    Splits large text into overlapping chunks using a sliding window.
    Overlap ensures meaning is preserved across chunk boundaries.
    """

    chunks = []                                     # List to store output chunks
    chunk_size = settings.CHUNK_SIZE                # e.g., 800 characters
    overlap = settings.CHUNK_OVERLAP                # e.g., 150 characters

    step = chunk_size - overlap                     # Sliding window step

    # Generate chunks using sliding window
    for start in range(0, len(text), step):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)

    return chunks
