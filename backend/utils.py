from huggingface_hub import InferenceClient
from transformers import CLIPModel, CLIPProcessor
from PIL import ImageOps, Image
import os
from uuid import uuid4
import torch
from torch.nn.functional import cosine_similarity

# Hugging Face 모델 설정
model_name = "black-forest-labs/FLUX.1-dev"
token = "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"
# InferenceClient 인스턴스 생성
client = InferenceClient(model_name, token=token)

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUTPUT_DIR = os.path.join(BASE_DIR, "generated_images")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Function to generate image from text
def generate_image(text):
    try:
        # 텍스트를 이미지로 변환
        image = client.text_to_image(text)
        file_path = os.path.join(OUTPUT_DIR, f"{uuid4()}.png")
        image.save(file_path)
        print(f"Image saved to {file_path}")
        return file_path
    except Exception as e:
        print(f"Error details: {str(e)}")
        raise Exception(f"Error generating image: {str(e)}")

# CLIP 모델과 프로세서 설정
clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32", cache_dir="./model_cache")
clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32", cache_dir="./model_cache")

def preprocess_text(text):
    max_length = 77
    return text[:max_length].strip()

def preprocess_image(image_path):
    try:
        image = Image.open(image_path).convert("RGB")  # RGB로 변환
        image = ImageOps.exif_transpose(image)  # EXIF 데이터를 반영하여 이미지 회전 문제 해결
        image = image.resize((224, 224))  # 모델 입력 크기에 맞게 이미지 크기 조정
        return image
    except Exception as e:
        raise Exception(f"Error preprocessing image: {str(e)}")

# Function to calculate similarity between image and text
def calculate_similarity(image_path, text):
    try:
        print(f"Calculating similarity for text: {text},  image: {image_path}")
        
         # 텍스트 및 이미지 확인
        if not os.path.exists(image_path):
            print(f"Image file not found at: {image_path}")
            raise FileNotFoundError(f"Image file not found at: {image_path}")
        
        text = preprocess_text(text)
        print(f"Preprocessed text: {text}")
        image = preprocess_image(image_path)
        print(f"Preprocessed image size: {image.size}")
        inputs = clip_processor(text=[text], images=[image], return_tensors="pt", padding=True)
        print(f"Inputs to CLIP model: {inputs}")
        print(f"Text tokenized inputs: {inputs['input_ids']}")
        print(f"Image tensor shape: {inputs['pixel_values'].shape}")
        
        outputs = clip_model(**inputs)
        print(f"CLIP outputs: {outputs}")
        
        image_embeds = outputs.image_embeds
        text_embeds = outputs.text_embeds

        sim = cosine_similarity(image_embeds, text_embeds).item()

        return sim
    except Exception as e:
        raise Exception(f"Error calculating similarity: {str(e)}")