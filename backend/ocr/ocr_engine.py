import pytesseract
from PIL import Image
from pdf2image import convert_from_path
import os

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text(path):
    ext = os.path.splitext(path)[1].lower()
    text = ""

    if ext == ".pdf":
        images = convert_from_path(path, dpi=300)
        for img in images:
            text += pytesseract.image_to_string(img) + "\n"

    elif ext in [".jpg", ".jpeg", ".png"]:
        image = Image.open(path)
        text = pytesseract.image_to_string(image)

    else:
        raise ValueError(f"Unsupported file type: {ext}")

    return text.strip()
