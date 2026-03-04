import cv2
import pytesseract
import os
import platform
from .text_runtime import detect_spam_from_text

if platform.system() == "Windows":
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def preprocess_image(image_path: str):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    return thresh

def detect_spam_from_image(image_path: str):

    processed = preprocess_image(image_path)
    extracted_text = pytesseract.image_to_string(processed).strip()

    if not extracted_text:
        return {
            "status": "error",
            "message": "No readable text found."
        }

    result = detect_spam_from_text(extracted_text)
    result["extracted_text"] = extracted_text[:300]

    return result