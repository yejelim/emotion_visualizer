# backend/utils.py

from transformers import CLIPProcessor, CLIPModel
import torch

# Load the CLIP model and processor
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch16")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch16")

def text_to_image_embeddings(text):
    inputs = processor(text=text, return_tensors="pt")
    text_embeddings = model.get_text_features(**inputs)
    return text_embeddings

def image_to_text_embeddings(image):
    inputs = processor(images=image, return_tensors="pt")
    image_embeddings = model.get_image_features(**inputs)
    return image_embeddings

def calculate_similarity(text_embeddings, image_embeddings):
    # Implement similarity calculation
    similarity = torch.nn.functional.cosine_similarity(text_embeddings, image_embeddings)
    return similarity
