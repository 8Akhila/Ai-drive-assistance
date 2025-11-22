# backend/app/extractors/ocr_extractor.py

import pytesseract
from PIL import Image

def extract_image_text(path: str) -> str:
    """
    Extract text from image files using OCR (Tesseract).
    Supports PNG, JPG, JPEG.
    """

    try:
        img = Image.open(path)
        text = pytesseract.image_to_string(img)
        return text.strip()
    except Exception as e:
        print(f"❌ OCR extraction failed: {e}")
        return ""
