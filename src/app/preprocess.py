import cv2
import numpy as np
from PIL import Image

def preprocess_image(img: Image.Image) -> Image.Image:
    img = img.convert("RGB")

    # Resize for speed
    w, h = img.size
    if w > 1200:
        ratio = 1200 / w
        img = img.resize((1200, int(h * ratio)))

    cv_img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    return Image.fromarray(gray)
