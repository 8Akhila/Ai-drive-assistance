"""
Google Drive → OCR → Text → Embedding → FAISS

This file handles:
✔ Downloading files
✔ Extracting text (OCR or parsing)
✔ Chunking text
✔ Embedding chunks
✔ Saving them to FAISS
✔ Remembering which files are already processed
"""

import os
import io
import json
from googleapiclient.http import MediaIoBaseDownload

from backend.app.drive.drive_client import get_drive_service
from backend.app.extractors.extractor import Extractor
from backend.app.embeddings.embedder import EmbeddingModel
from backend.app.processing.chunker import chunk_text
from backend.app.vectorstore.faiss_store import FaissStore


extractor = Extractor()
embedder = EmbeddingModel()
faiss_store = FaissStore()

RAW_DIR = "backend/app/data/raw"
PROCESSED_FILE = "backend/app/data/processed_files.json"

os.makedirs(RAW_DIR, exist_ok=True)


def load_processed():
    """Returns dictionary of previously synced files."""
    if not os.path.exists(PROCESSED_FILE):
        return {}
    try:
        with open(PROCESSED_FILE, "r") as f:
            return json.load(f)
    except:
        return {}


def save_processed(data):
    """Writes processed file list."""
    with open(PROCESSED_FILE, "w") as f:
        json.dump(data, f, indent=4)


def sync_drive_files():
    """Main synchronization pipeline."""

    print("\n⚡ SYNC STARTED...\n")
    processed = load_processed()

    mime_types = [
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "text/plain",
        "image/png",
        "image/jpeg",
        "video/mp4",
        "video/quicktime",
    ]

    query = " or ".join([f"mimeType='{m}'" for m in mime_types])
    service = get_drive_service()

    files = service.files().list(q=query).execute().get("files", [])
    print(f"🔵 Total files detected: {len(files)}")

    new_indexed = 0

    for f in files:
        file_name = f["name"]
        file_id = f["id"]
        file_path = os.path.join(RAW_DIR, file_name)

        if file_name in processed:
            print(f"⏭ Skipping (already indexed): {file_name}")
            continue

        print(f"\n📌 Processing: {file_name}")

        # Download
        req = service.files().get_media(fileId=file_id)
        with io.FileIO(file_path, "wb") as fh:
            downloader = MediaIoBaseDownload(fh, req)
            done = False
            while not done:
                _, done = downloader.next_chunk()

        print("   ✔ Download complete")

        # Extract text
        text = extractor.extract(file_path)

        if not text.strip():
            text = f"[NO OCR TEXT] File: {file_name}"

        chunks = chunk_text(text)
        print(f"   📚 {len(chunks)} chunks created")

        batch_vecs, batch_meta = [], []

        for chunk in chunks:
            batch_vecs.append(embedder.embed(chunk))
            batch_meta.append({
                "file_name": file_name,
                "file_id": file_id,
                "snippet": chunk[:250],
                "drive_link": f"https://drive.google.com/file/d/{file_id}"
            })

        faiss_store.add_batch(batch_vecs, batch_meta)

        processed[file_name] = True
        save_processed(processed)
        new_indexed += 1

    print("\n✅ SYNC COMPLETE\n")

    return {
        "message": "Sync Finished",
        "new_files_indexed": new_indexed,
        "total_indexed": len(processed)
    }
