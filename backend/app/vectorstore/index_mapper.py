import json                                          # To load metadata JSON file
from backend.app.config import settings
def load_metadata_store():
    """
    Loads the metadata JSON file that maps chunk IDs → details.
    """

    try:
        with open(settings.METADATA_STORE, "r", encoding="utf-8") as f:
            return json.load(f)                      # Return metadata dictionary
    except FileNotFoundError:
        return {}                                     # If missing, return empty dict


def get_chunk_info(chunk_id: int):
    """
    Returns metadata for a given chunk ID.
    """

    metadata_store = load_metadata_store()            # Load metadata dictionary

    # Chunk IDs are saved as strings in JSON
    return metadata_store.get(str(chunk_id))          # Return chunk metadata
