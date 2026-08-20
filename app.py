import os

import streamlit as st
from PIL import Image, ImageOps

from ocr import extract_text
from translator import translate_menu

if "OPENAI_API_KEY" in st.secrets:
    os.environ.setdefault("OPENAI_API_KEY", st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="Menu Translator", page_icon="\U0001F37D️")
st.title("\U0001F37D️ Menu Translator")
st.caption(
    "Snap a photo of a foreign menu. Get the dish name, the translation, "
    "and what it is"
)

if not os.environ.get("OPENAI_API_KEY"):
    st.warning(
        "No OPENAI_API_KEY found.", icon="⚠️")

image_file = st.camera_input("Take a photo of the menu")

if image_file is None:
    st.caption("No camera? Upload a photo instead:")
    image_file = st.file_uploader(
        "Upload a menu photo", type=["jpg", "jpeg", "png"], label_visibility="collapsed"
    )

if image_file is not None:
    image = ImageOps.exif_transpose(Image.open(image_file))
    st.image(image, caption="Captured menu", use_container_width=True)

    if st.button("Translate menu", type="primary"):
        with st.spinner("Reading menu..."):
            raw_text = extract_text(image)

        if not raw_text.strip():
            st.error(
                "Couldn't read any text from that photo. Try a flatter angle, "
                "better lighting, or move closer."
            )
        else:
            with st.expander("Raw OCR text"):
                st.text(raw_text)

            with st.spinner("Translating and explaining..."):
                try:
                    dishes = translate_menu(raw_text)
                except Exception as e:  # send API/parsing error to the UI
                    st.error(f"Something went wrong calling OpenAI: {e}")
                    dishes = []

            if not dishes:
                st.info("No dishes recognized in that text yet.")

            for dish in dishes:
                with st.container(border=True):
                    st.subheader(dish.get("original", "?"))
                    st.markdown(f"**Translation:** {dish.get('translation', '?')}")
                    st.markdown(f"**What it actually is:** {dish.get('explanation', '?')}")
