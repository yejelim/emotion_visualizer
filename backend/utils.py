# backend/utils.py

from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer
import torch
from diffusers import StableDiffusionPipeline


# Load the Stable Diffusion model
sd_pipeline = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4")
sd_pipeline.to("cuda")

# Load image captioning model
caption_model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
image_processor = ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")


def generate_image_from_text(text):
    image = sd_pipeline(text).images[0]
    return image

def generate_text_from_image(image):
    pixel_values = image_processor(images=image, return_tensors="pt").pixel_values
    output_ids = caption_model.generate(pixel_values)
    caption = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return caption