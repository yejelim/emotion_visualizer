# Backend/main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from utils import generate_image, calculate_similarity
import os

app = FastAPI()

# 한 번만 session_data 정의
session_data = {}

class TextInput(BaseModel):
    prompt: str

class DetailedInput(BaseModel):
    image_path: str
    detailed_text: str

@app.post("/generate-image/")
async def generate_image_endpoint(request: TextInput):
    try:
        # 디버깅용: 요청 받은 prompt 출력
        print(f"[DEBUG] generate-image received prompt: {request.prompt}")

        # 이미지 생성
        image_path = generate_image(request.prompt)
        print(f"[DEBUG] Image saved at: {image_path}")

        # 유사도 계산
        initial_similarity = calculate_similarity(image_path, request.prompt)
        print(f"[DEBUG] Initial similarity: {initial_similarity}")

        # 세션 ID 생성 및 저장
        session_id = os.path.basename(image_path).split(".")[0]
        session_data[session_id] = {
            "image_path": image_path,
            "prompt": request.prompt,
            "initial_similarity": initial_similarity,
        }
        print(f"[DEBUG] Session {session_id} stored: {session_data[session_id]}")
        print(f"[DEBUG] Current session_data keys after store: {list(session_data.keys())}")

        return {
            "session_id": session_id,
            "image_path": image_path,
            "initial_similarity": initial_similarity,
        }
    except Exception as e:
        print(f"[ERROR] In generate_image_endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze-detailed-text/")
async def analyze_detailed_text(request: DetailedInput):
    try:
        # 디버깅용: 요청 받은 정보 출력
        print(f"[DEBUG] analyze-detailed-text received:")
        print(f"    image_path: {request.image_path}")
        print(f"    detailed_text: {request.detailed_text}")

        # 현재 session_data 키 확인
        print(f"[DEBUG] Current session_data keys: {list(session_data.keys())}")

        # 세션에서 session_id 추출
        session_id = request.image_path.split("/")[-1].split(".")[0]
        print(f"[DEBUG] Extracted session_id from image_path: {session_id}")

        if session_id not in session_data:
            print(f"[ERROR] Session not found: {session_id}")
            raise HTTPException(status_code=404, detail="Session not found.")
        
        session = session_data[session_id]
        print(f"[DEBUG] Found session data: {session}")

        # 유사도 계산
        detailed_similarity = calculate_similarity(session["image_path"], request.detailed_text)
        improvement = (detailed_similarity - session["initial_similarity"]) * 100
        print(f"[DEBUG] Detailed similarity: {detailed_similarity}, Improvement: {improvement}")

        return {
            "detailed_similarity": detailed_similarity,
            "improvement": improvement,
        }
    except Exception as e:
        print(f"[ERROR] In analyze_detailed_text: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error analyzing description: {str(e)}")

@app.get("/check-sessions/")
async def check_sessions():
    print(f"[DEBUG] Current session data: {session_data}")
    return session_data
