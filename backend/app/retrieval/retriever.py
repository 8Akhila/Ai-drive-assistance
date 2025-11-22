import json                                          # For reading metadata JSON file
from backend.app.config import settings
def load_metadata():
    """
    Loads the metadata JSON file that contains a list of chunks.
    Each chunk includes: text, file_name, file_id, etc.
    """

    try:
        # Open and read metadata JSON file
        with open(settings.METADATA_STORE, "r", encoding="utf-8") as f:
            return json.load(f)                      # Return parsed metadata as dict

    except FileNotFoundError:
        # If no metadata file exists yet, return empty dictionary
        return {}


def retrieve_chunks(faiss_ids: list[int]):
    """
    Given a list of FAISS vector IDs, fetch the corresponding chunk metadata.
    """

    metadata = load_metadata()                        # Load stored chunk information
    results = []                                      # List to store matching chunk entries

    for idx in faiss_ids:                             # Loop through each FAISS ID
        chunk_info = metadata.get(str(idx))           # Metadata stored with string keys

        if chunk_info:
            results.append(chunk_info)                # Add metadata entry to result list

    return results                                     # Return list of metadata chunks
