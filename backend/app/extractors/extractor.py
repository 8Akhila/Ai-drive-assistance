"""
Unified Extractor Interface (Windows-Safe Version WITH VIDEO SUPPORT)

Handles:
✔ PDF
✔ DOCX
✔ TXT
✔ Images → OCR using Tesseract
✔ Videos → Placeholder text (Windows does not support Whisper)

This extractor auto-selects the correct parser based on file extension.
"""

import os

# Import specific working extractors
from backend.app.extractors.pdf_extractor import extract_pdf_text
from backend.app.extractors.docx_extractor import extract_docx_text
from backend.app.extractors.ocr_extractor import extract_image_text


class Extractor:

    def __init__(self):
        """
        Maps supported file extensions to extraction functions.
        Makes the system modular & easy to expand later.
        """
        self.handlers = {
            # Document types
            "pdf": extract_pdf_text,
            "docx": extract_docx_text,
            "doc": extract_docx_text,
            "txt": self._read_text,

            # Image OCR
            "png": extract_image_text,
            "jpg": extract_image_text,
            "jpeg": extract_image_text,

            # Video formats (placeholder only - no transcription on Windows)
            "mp4": self._video_placeholder,
            "mov": self._video_placeholder,
            "avi": self._video_placeholder,
            "mkv": self._video_placeholder,
        }

    def _read_text(self, path: str) -> str:
        """Reads plain text files safely with UTF-8 handling."""
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except:
            try:
                with open(path, "r", errors="ignore") as f:
                    return f.read()
            except:
                return ""

    def _video_placeholder(self, path: str) -> str:
        """Returns placeholder when encountering a video file."""
        return "[VIDEO FILE – no transcription available on Windows]"

    def extract(self, path: str) -> str:
        """
        Main public method.
        Detects file extension and calls correct extractor.
        Fallback: treat file as plain text.
        """

        if not os.path.exists(path):
            return ""

        ext = os.path.splitext(path)[1].lower().lstrip(".")
        handler = self.handlers.get(ext)

        if handler is None:
            return self._read_text(path)

        try:
            return handler(path)
        except Exception:
            return self._read_text(path)
