# frontend/app.py

import streamlit as st
import requests

st.title("Emotion Visualizer")

option = st.selectbox(
    "Choose an option:",
    ("Text to Image", "Image to Text"),
    key='main_selectbox'
)

if option == "Text to Image":
    text_input = st.text_input("Enter your emotion:", key='text_input_enter')
    if st.button("Visualize Emotion", key='visualize_button'):
        if text_input.strip() == "":
            st.warning("Please enter an emotion.")
        else:
            response = requests.post(
                "http://localhost:8000/text-to-image",
                json={"text": text_input}
            )
            if response.status_code == 200:
                # Display the image (placeholder)
                st.image(response.content, use_container_width=True)
            else:
                st.error("Failed to generate image.")
                
elif option == "Image to Text":
    uploaded_file = st.file_uploader("Upload an image:", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        if st.button("Analyze Emotion", key='analyze_button'):
            files = {'file': uploaded_file.getvalue()}
            response = requests.post(
                "http://localhost:8000/image-to-text",
                files=files
            )
            # Display the text analysis
            st.write(response.text)
