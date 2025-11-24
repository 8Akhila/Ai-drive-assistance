"""
Unified Extractor Engine with Automatic File Detection.
Supports:
✔ Image OCR (Tesseract)
✔ PDF text extraction
✔ DOC/DOCX extraction
✔ Plain text files
✔ Video placeholder

This ensures OCR gets triggered correctly for images.
"""

import os
import mimetypes

# Import specific extractors
from backend.app.extractors.pdf_extractor import extract_pdf_text
from backend.app.extractors.docx_extractor import extract_docx_text
from backend.app.extractors.ocr_extractor import extract_image_text


class Extractor:

    def extract(self, path: str) -> str:
        """
        Main entry for extraction.
        Detects MIME type and chooses the correct extractor.
        """

        if not os.path.exists(path):
            print(f"❌ File not found: {path}")
            return ""

        mime_type = mimetypes.guess_type(path)[0]

        # Fallback if mimetype detection fails
        if mime_type is None:
            return self._read_text(path)

        # ----- IMAGE OCR -----
        if mime_type.startswith("image"):
            print(f"🧠 OCR Processing Image → {os.path.basename(path)}")
            return extract_image_text(path)

        # ----- PDF -----
        if mime_type == "application/pdf":
            print(f"📄 Extracting PDF → {os.path.basename(path)}")
            return extract_pdf_text(path)

        # ----- DOCX -----
        if mime_type.endswith("wordprocessingml.document"):
            print(f"📝 Extracting DOCX → {os.path.basename(path)}")
            return extract_docx_text(path)

        # ----- Plain Text -----
        if mime_type.startswith("text"):
            print(f"📄 Reading Text File → {os.path.basename(path)}")
            return self._read_text(path)

        # 🔄 Default fallback
        return self._read_text(path)

    def _read_text(self, path: str) -> str:
        """Safe fallback text reader for unknown formats."""
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()
        except:
            return ""
