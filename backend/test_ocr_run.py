from backend.app.extractors.ocr_extractor import extract_image_text

# Change this file path to one of the real images already in /data/raw
test_image = r"backend/app/data/raw/Pan card.jpg"

print("\n🔍 Testing OCR on:", test_image)
result = extract_image_text(test_image)

if result.strip():
    print("\n✅ OCR SUCCESS — Extracted Text:\n")
    print(result)
else:
    print("\n❌ OCR FAILED — No readable text extracted.")
