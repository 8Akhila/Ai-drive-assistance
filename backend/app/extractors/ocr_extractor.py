# backend/app/extractors/ocr_extractor.py

import pytesseract
from PIL import Image

# REQUIRED FOR WINDOWS — update if installed elsewhere
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def extract_image_text(path: str) -> str:
    """
    Extracts readable text from JPEG / JPG / PNG images.
    Uses Tesseract OCR.
    """

    try:
        img = Image.open(path)
        img = img.convert("RGB")  # Prevent mode errors
        text = pytesseract.image_to_string(img)
        return text.strip()
    except Exception as e:
        print(f"❌ OCR Failed for {path}: {e}")
        return ""
