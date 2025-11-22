import os
import json
from backend.app.config import settings
def save_metadata(metadata_list: list[dict]):
    """
    Saves list of chunk metadata dictionaries into a JSON file.
    This metadata is used later by the retriever to map FAISS IDs → text.
    """

    # Create storage directory if missing
    os.makedirs(os.path.dirname(settings.METADATA_STORE), exist_ok=True)

    # Write metadata list to JSON file
    with open(settings.METADATA_STORE, "w", encoding="utf-8") as f:
        json.dump(metadata_list, f, indent=2)  # Pretty print for readability


def build_metadata(chunks: list[str], file_name: str, file_id: str):
    """
    Creates metadata entries for each chunk of a file.
    """

    metadata_list = []   # Store all chunk metadata entries

    for idx, chunk in enumerate(chunks):
        # Create dictionary for each chunk
        metadata = {
            "chunk_id": idx,          # Numerical ID of this chunk
            "file_name": file_name,   # Original file name
            "file_id": file_id,       # Drive ID to open the file
            "text": chunk,            # Actual chunk text
            "page": None              # Can be filled if PDF page numbers added later
        }

        metadata_list.append(metadata)  # Add entry to metadata list

    return metadata_list                # Return metadata for calling function
