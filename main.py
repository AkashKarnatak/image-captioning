import streamlit as st
import os
from PIL import Image
import glob


def load_images_and_captions(directory, trigger_word):
    image_files = []
    for ext in ["*.jpg", "*.jpeg", "*.png", "*.gif"]:
        image_files.extend(glob.glob(os.path.join(directory, ext)))

    images_and_captions = []
    for img_path in sorted(image_files):
        caption_path = os.path.splitext(img_path)[0] + ".txt"

        caption = trigger_word
        if os.path.exists(caption_path):
            with open(caption_path, "r", encoding="utf-8") as f:
                caption = f.read().strip()
                caption = caption or trigger_word

        images_and_captions.append(
            {"image_path": img_path, "caption_path": caption_path, "caption": caption}
        )

    return images_and_captions


def save_captions(captions_data):
    for item in captions_data:
        with open(item["caption_path"], "w", encoding="utf-8") as f:
            f.write(item["caption"])


def main():
    st.set_page_config(layout="wide", page_title="Image Caption Tool")

    st.title("Image Captioning Tool")
    st.markdown("---")

    with st.sidebar:
        st.header("Controls")
        directory = st.text_input("Image Directory")
        trigger_word = st.text_input("Trigger word", value="p3rs0n")
        col1, col2 = st.columns(2)
        with col1:
            load_button = st.button("Load Images", type="primary")
        with col2:
            save_button = st.button("Save All", type="primary")

    if "images_and_captions" not in st.session_state:
        st.session_state.images_and_captions = []

    if load_button and directory and trigger_word:
        with st.spinner("Loading images..."):
            st.session_state.images_and_captions = load_images_and_captions(
                directory, trigger_word
            )
        st.success(f"Loaded {len(st.session_state.images_and_captions)} images")

    if save_button:
        with st.spinner("Saving captions..."):
            save_captions(st.session_state.images_and_captions)
        st.success("All captions saved successfully!")

    if st.session_state.images_and_captions:
        for idx, item in enumerate(st.session_state.images_and_captions):
            col1, col2 = st.columns([1, 3])

            with col1:
                image = Image.open(item["image_path"])
                st.image(image, width=200)
                st.caption(os.path.basename(item["image_path"]))

            with col2:
                new_caption = st.text_area(
                    "Caption", value=item["caption"], key=f"caption_{idx}", height=100
                )
                st.session_state.images_and_captions[idx]["caption"] = new_caption

    elif directory:
        st.info(
            "No images found in the selected directory. Make sure the directory contains supported image files (jpg, jpeg, png, gif)."
        )
    else:
        st.info("Please enter a directory path and click 'Load Images' to start.")


if __name__ == "__main__":
    main()
