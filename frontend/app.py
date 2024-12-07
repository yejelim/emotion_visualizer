import streamlit as st
import requests
import os

# Streamlit 제목 설정
st.title("Emotion Visualizer")

# 세션 상태 초기화
if "session_id" not in st.session_state:
    st.session_state["session_id"] = None
if "image_path" not in st.session_state:
    st.session_state["image_path"] = None
if "initial_similarity" not in st.session_state:
    st.session_state["initial_similarity"] = None

# 텍스트 입력 상자
text_input = st.text_input("Describe your emotion:")

# **1단계: 이미지 생성**
if st.button("Generate Visualization"):
    if text_input.strip() == "":
        st.warning("Please enter a description.")
    else:
        response = requests.post(
            "http://localhost:8000/generate-image/",
            json={"prompt": text_input}
        )

        if response.status_code == 200:
            data = response.json()
            st.session_state["session_id"] = data["session_id"]
            st.session_state["image_path"] = data["image_path"]
            st.session_state["initial_similarity"] = data["initial_similarity"]

            # 이미지 표시
            st.image(
                st.session_state["image_path"], 
                caption="Generated Image", 
                use_column_width=True
            )
            st.write(f"Initial similarity: {st.session_state['initial_similarity']:.2f}")
        else:
            st.error("Failed to generate image.")

# **2단계: 이미지 설명 입력**
if st.session_state["session_id"] and st.session_state["image_path"]:
    st.write("Now, describe the image in more detail:")
    detailed_input = st.text_input("Detailed description:", key="detailed_input")

    # 유사도 계산
    if st.button("Submit"):
        if detailed_input.strip() == "":
            st.warning("Please provide a detailed description.")
        else:
            response = requests.post(
                "http://localhost:8000/analyze-detailed-text/",
                json={
                    "image_path": st.session_state["image_path"], 
                    "detailed_text": detailed_input
                }
            )

            if response.status_code == 200:
                data = response.json()
                detailed_similarity = data["detailed_similarity"]
                improvement = data["improvement"]

                # 결과 표시
                st.write(f"Detailed similarity: {detailed_similarity:.2f}")
                st.success(f"Your expression accuracy improved by {improvement:.2f}%.")
            else:
                st.error("Failed to analyze detailed description.")
