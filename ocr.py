import cv2
import numpy as np
import pytesseract
from PIL import Image

def preprocess_image(image: Image.Image) -> Image.Image: #preprocess for better result

    img = np.array(image.convert("RGB"))
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY) #grayscale 

    # upscale small images
    scale = 2
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


def extract_text(image: Image.Image, lang: str = "eng+chi_sim+chi_tra+hin+spa+ara+fra+ben+por+rus+urd") -> str:
    processed = preprocess_image(image)
    return pytesseract.image_to_string(processed, lang=lang)
