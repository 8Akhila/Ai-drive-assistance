"""
This module decides WHICH extractor to use based on the file extension.
It routes PDF → pdf_extractor, DOCX → docx_extractor, images → OCR,
videos → transcription, etc.
"""

import os

# Correct imports using full path "backend.app..."
from backend.app.extractors.pdf_extractor import extract_pdf_text      # PDF text extraction
from backend.app.extractors.docx_extractor import extract_docx_text    # Word Doc extraction
from backend.app.extractors.ocr_extractor import extract_image_text    # OCR for images
from backend.app.extractors.video_transcriber import transcribe_video  # Transcribe video/audio


def extract_text(file_path: str) -> str | None:
    """
    Detects the file type from its extension and calls the correct extractor.
    Returns extracted text OR None if unsupported.
    """

    # Get extension → .pdf, .docx, .png, .mp4 etc.
    _, ext = os.path.splitext(file_path)
    ext = ext.lower().strip()

    # ----------------------------
    #  PDF    → Text Extraction
    # ----------------------------
    if ext == ".pdf":
        return extract_pdf_text(file_path)

    # ----------------------------
    #  Word Document (.docx)
    # ----------------------------
    elif ext == ".docx":
        return extract_docx_text(file_path)

    # ----------------------------
    #  Images → OCR extraction
    # ----------------------------
    elif ext in [".png", ".jpg", ".jpeg"]:
        return extract_image_text(file_path)

    # ----------------------------
    # Video files → Speech → Text
    # ----------------------------
    elif ext in [".mp4", ".mkv", ".mov"]:
        return transcribe_video(file_path)

    # ----------------------------
    # Unsupported type
    # ----------------------------
    else:
        print(f"[Extractor] Unsupported file type: {ext}")
        return None
