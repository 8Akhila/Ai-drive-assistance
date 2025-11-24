import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

path = r"backend/app/data/raw/Pan card.jpg" # change if needed
text = pytesseract.image_to_string(Image.open(path))
print(text)
