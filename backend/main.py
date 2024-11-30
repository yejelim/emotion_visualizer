# backend/main.py

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse, PlainTextResponse
from pydantic import BaseModel
from utils import generate_image_from_text, generate_text_from_image
from PIL import Image
import io

app = FastAPI()

class TextInput(BaseModel):
    text: str

@app.post("/text-to-image")
async def text_to_image_endpoint(text_input: TextInput):
    image = generate_image_from_text(text_input.text)
    # Save or process the image as needed
    # For example, convert to bytes and return
    buf = io.BytesIO()
    image.save(buf, format='PNG')
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")

@app.post("/image-to-text")
async def image_to_text_endpoint(file: UploadFile = File(...)):
    try:
        image = Image.open(io.BytesIO(await file.read())).convert("RGB")
    except Exception as e:
        return PlainTextResponse(f"Error processing image: {str(e)}", status_code=400)
        
    caption = generate_text_from_image(image)
    # Return the caption as plain text
    return PlainTextResponse(caption)


@app.get("/health")
async def health_check():
    return {"status": "OK"}
