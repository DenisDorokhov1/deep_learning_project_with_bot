import torch
import numpy as np
from PIL import Image
from transformers import AutoImageProcessor, AutoModel

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
MODEL_NAME = "facebook/dinov2-base"

processor = AutoImageProcessor.from_pretrained(MODEL_NAME, use_fast=True)
model = AutoModel.from_pretrained(MODEL_NAME).to(DEVICE)
model.eval()

def encode_image(image_path: str) -> np.ndarray:
    image = Image.open(image_path).convert("RGB")

    inputs = processor(images=image, return_tensors="pt").to(DEVICE)

    with torch.no_grad():
        outputs = model(**inputs)

    embedding = outputs.last_hidden_state.mean(dim=1)
    embedding = embedding / embedding.norm(dim=-1, keepdim=True)

    return embedding.cpu().numpy().astype("float32")[0]
