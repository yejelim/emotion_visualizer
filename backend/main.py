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
    # Process the text input and generate an image (placeholder logic)
    text_embeddings = text_to_image_embeddings(text_input.text)
    # Implement your custom logic here
    return {"message": "Image generated based on text."}

@app.post("/image-to-text")
async def image_to_text_endpoint(file: UploadFile = File(...)):
    image = Image.open(io.BytesIO(await file.read()))
    image_embeddings = image_to_text_embeddings(image)
    # Implement your custom logic here
    return {"message": "Text generated based on image."}

@app.get("/health")
async def health_check():
    return {"status": "OK"}
