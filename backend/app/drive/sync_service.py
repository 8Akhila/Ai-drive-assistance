"""
Sync Service: Extract → Detect IDs → Chunk → Embed → FAISS Store
"""

import os
import io
import json
from googleapiclient.http import MediaIoBaseDownload

from backend.app.drive.drive_client import get_drive_service
from backend.app.extractors.extractor import Extractor
from backend.app.extractors.id_extractor import extract_ids
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
    if not os.path.exists(PROCESSED_FILE):
        return {}
    try:
        return json.load(open(PROCESSED_FILE, "r"))
    except:
        return {}


def save_processed(data):
    json.dump(data, open(PROCESSED_FILE, "w"), indent=4)


def sync_drive_files():

    print("\n⚡ SYNC STARTED...\n")

    processed = load_processed()
    drive_service = get_drive_service()

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

    files = drive_service.files().list(q=query).execute().get("files", [])
    print(f"🔍 {len(files)} files detected in Drive")

    new_indexed = 0

    for f in files:

        file_name = f["name"]
        file_id = f["id"]
        file_path = os.path.join(RAW_DIR, file_name)

        if file_name in processed:
            print(f"⏭ Already indexed → {file_name}")
            continue

        print(f"\n📌 Processing → {file_name}")

        request = drive_service.files().get_media(fileId=file_id)
        with io.FileIO(file_path, "wb") as fh:
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while not done:
                _, done = downloader.next_chunk()

        print("   ✔ Downloaded")

        # ----- Extract text -----
        raw_text = extractor.extract(file_path)
        if not raw_text.strip():
            raw_text = "[NO OCR TEXT FOUND]"

        # ----- Extract IDs (PAN, Aadhaar, Phone Numbers) -----
        detected_ids = extract_ids(raw_text)
        print(f"   🔍 IDs found: {detected_ids}")

        combined_text = raw_text + "\n\n[DETECTED IDs] " + json.dumps(detected_ids)

        # ----- Chunk for embedding -----
        chunks = chunk_text(combined_text)
        print(f"   📦 {len(chunks)} chunks created")

        embeddings, metadata = [], []

        for chunk in chunks:
            embeddings.append(embedder.embed(chunk))
            metadata.append({
                "file_name": file_name,
                "file_id": file_id,
                "snippet": chunk[:2000],
                "ids": detected_ids,
                "drive_link": f"https://drive.google.com/file/d/{file_id}"
            })

        faiss_store.add_batch(embeddings, metadata)

        processed[file_name] = True
        save_processed(processed)
        new_indexed += 1

    print("\n✅ SYNC COMPLETE\n")

    return {
        "message": "Sync Finished",
        "files_added_this_run": new_indexed,
        "total_files_indexed": len(processed)
    }
