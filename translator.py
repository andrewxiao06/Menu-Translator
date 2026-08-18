import json
import os

from openai import OpenAI

MODEL = "gpt-4o-mini"

SYSTEM_PROMPT = """You are reading raw, possibly noisy OCR text extracted from a \
photograph of a restaurant menu. The menu may be in any language and the OCR \
text may contain errors: misread characters, garbled spacing, stray symbols.

For each distinct dish or menu item you can identify, produce:
1. "original": the dish name as best you can reconstruct it in its original language
2. "translation": an accurate English translation of the dish name
3. "explanation": one short, plain English sentence describing what the dish \
   actually is (main ingredients, how it's typically prepared or served) - the \
   kind of context a local friend would give a confused tourist.

Ignore prices, section headers (e.g. "APPETIZERS"), and OCR noise that isn't \
actually a dish name.

Return ONLY a JSON object of this exact shape, nothing else:
{"dishes": [{"original": "...", "translation": "...", "explanation": "..."}]}
"""


def translate_menu(raw_text: str, api_key: str | None = None) -> list[dict]:
    """Send raw OCR text to OpenAI and get back structured dish translations.

    Returns a list of {"original", "translation", "explanation"} dicts.
    Or raises an error
    """
    client = OpenAI(api_key=api_key) or OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    response = client.chat.completions.create(
        model=MODEL,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": raw_text},
        ],
    )

    content = response.choices[0].message.content
    data = json.loads(content)
    return data.get("dishes", [])
