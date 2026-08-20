Point your camera at a foreign menu. Get the dish name, the translation, and what it is.

# Stack

- **Streamlit** - UI, camera capture (`st.camera_input`), results display
- **Tesseract** (`pytesseract`) - OCR on the photo
- **OpenAI** (`gpt-4o-mini`) - one structured call that translates each
  dish and explains what it is, in the same pass

# How it works

1. User takes a single photo with `st.camera_input`
2. `ocr.py` preprocesses the image and runs Tesseract to get raw text.
3. `translator.py` sends that raw OCR text to OpenAI with a prompt asking
   for structured JSON: original dish name, English translation, and a
   one-sentence explanation of what the dish actually is.
4. `app.py` renders the results as cards.

## Local setup

```bash

#for mac
brew install tesseract

#Create venv and install dependencies
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

#add openai key

# run
streamlit run app.py
```

## Known scope / risk areas

Use French, Spanish, or Italian where Tesseract is much more reliable.

- **v1 is English-OCR-only** (`lang="eng"` in `ocr.py::extract_text`). To
  read non-Latin menus you need the matching Tesseract language pack
  installed

THEN

Deploy onto Streamlit Community and link it to your github account so you can use this on your phone with a live website url
