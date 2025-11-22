"""
Config helper: reads environment variables and provides defaults.
"""

import os

class Settings:
    # Drive credential paths (absolute recommended)
    GOOGLE_CREDENTIALS_PATH = os.environ.get("GOOGLE_CREDENTIALS_PATH", "C:/Users/AKHILA/drive-ai-agent/credentials.json")
    GOOGLE_TOKEN_PATH = os.environ.get("GOOGLE_TOKEN_PATH", "C:/Users/AKHILA/drive-ai-agent/token.json")

    RAW_FILES_PATH = os.environ.get("RAW_FILES_PATH", "data/raw_files")
    EXTRACTED_TEXT_PATH = os.environ.get("EXTRACTED_TEXT_PATH", "data/extracted_texts")
    TRANSCRIPTS_PATH = os.environ.get("TRANSCRIPTS_PATH", "data/transcripts")

    CHUNK_SIZE = int(os.environ.get("CHUNK_SIZE", "800"))
    CHUNK_OVERLAP = int(os.environ.get("CHUNK_OVERLAP", "150"))

    EMBEDDING_MODEL = os.environ.get("EMBEDDING_MODEL", "sentence-transformers/all-mpnet-base-v2")
    VECTOR_INDEX_PATH = os.environ.get("VECTOR_INDEX_PATH", "backend/app/storage/faiss.index")
    METADATA_STORE = os.environ.get("METADATA_STORE", "backend/app/storage/metadata_store.json")

    # LLM settings
    LLM_PROVIDER = os.environ.get("LLM_PROVIDER", "openai")
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

settings = Settings()
