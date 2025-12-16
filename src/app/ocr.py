import pytesseract

def run_ocr(img):
    text = pytesseract.image_to_string(img)
    return text.upper()
