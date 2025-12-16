from PIL import Image
from app.preprocess import preprocess_image
from app.ocr import run_ocr
from app.extractor import extract_fields
import sys

img = Image.open(sys.argv[1]).convert("RGB")
img = preprocess_image(img)
text = run_ocr(img)
print(extract_fields(text))
