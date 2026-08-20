import cv2
import numpy as np
import pytesseract
from PIL import Image

def preprocess_image(image: Image.Image) -> Image.Image: #preprocess for better result

    img = np.array(image.convert("RGB"))
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY) #grayscale 

    # upscale only if the source photo is small - phone photos are already
    # high-res, and upscaling those can blow past Tesseract's limits and
    # cause it to miss parts of the menu
    min_width = 1500
    if gray.shape[1] < min_width:
        scale = min_width / gray.shape[1]
        gray = cv2.resize(gray, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)

    thresh = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        15,
    )

    return Image.fromarray(thresh)


def extract_text(image: Image.Image, lang: str = "eng+dan+deu") -> str:
    processed = preprocess_image(image)
    return pytesseract.image_to_string(processed, lang=lang)
