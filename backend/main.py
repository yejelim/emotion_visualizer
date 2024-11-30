# backend/main.py

from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from utils import text_to_image_embeddings, image_to_text_embeddings
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
    image = Image.open(io.BytesIO(await file.read()))
    caption = generate_text_from_image(image)
    return {"description": caption}


@app.get("/health")
async def health_check():
    return {"status": "OK"}
