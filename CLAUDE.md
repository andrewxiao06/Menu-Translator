# Project context for Claude Code

point your camera at a foreign menu, get the
dish name, an English translation, and a one-sentence explanation of what
the dish actually is.

**Stack:** Python, Streamlit, Tesseract (`pytesseract`), OpenAI (`gpt-4o-mini`).

**Pipeline:** `st.camera_input` (single snapshot, not video) -> `ocr.py`
preprocesses + runs Tesseract -> `translator.py` sends the raw OCR text to
one OpenAI call that returns structured JSON (translation + explanation
per dish, in one pass) -> `app.py` renders it.

**Deliberate design decisions, don't relitigate these without a reason:**

- Single photo capture, not live video / AR overlay. That's a much bigger
  project and out of scope.
- Translation and "what is this" explanation are one combined LLM call,
  not a separate translation-API step + separate LLM step. The LLM
  tolerates OCR noise/typos better than a rigid parser would, and it's
  one API to debug instead of two.
- Currently English-OCR-only (`lang="eng"`). Multi-language support is a
  known v2 item, see the `TODO(v2)` comment in `app.py` and the "Ideas for
  v2" section in `README.md`.

**Known weak point:** Tesseract's accuracy on real photographed menus
(skew, glare, decorative fonts, non-Latin scripts) is the most likely
thing to make the demo look bad. See "Known scope / risk areas" in
`README.md` before spending a lot of time elsewhere in the pipeline.

**Status:** skeleton only, not yet run end-to-end. Priority order for a
first working pass: (1) confirm Tesseract installed locally and OCR
produces readable text on a real test photo, (2) confirm the OpenAI call
returns parseable JSON, (3) polish the UI, (4) deploy to Streamlit
Community Cloud.
