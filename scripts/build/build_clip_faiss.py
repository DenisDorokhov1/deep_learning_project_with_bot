import os
import zipfile
import shutil
import pandas as pd
from pathlib import Path
from collections import defaultdict
from PIL import Image
import numpy as np
from tqdm import tqdm
import faiss
from transformers import CLIPModel, CLIPProcessor
import torch
import json


# Пути относительно корня проекта
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

CSV_PATH = PROJECT_ROOT / "data" / "full_dataset.csv"
ZIP_PATH = PROJECT_ROOT / "images.zip"
IMG_DIR = PROJECT_ROOT / "images"
FAISS_INDEX_PATH = PROJECT_ROOT / "data" / "clip_data" / "monuments.faiss"
METADATA_PATH_CLIP = PROJECT_ROOT / "data" / "clip_data" / "monuments_metadata.json"
METADATA_PATH_ROOT = PROJECT_ROOT / "data" / "monuments_metadata.json"  # для бота


 # Загрузка CSV

df = pd.read_csv(CSV_PATH)


#Распаковка ZIP с фото, раскомментировать, если не делали вручную
# IMG_DIR.mkdir(parents=True, exist_ok=True)
#
# with zipfile.ZipFile(ZIP_PATH, 'r') as zip_ref:
#     for member in zip_ref.infolist():
#         filename = os.path.basename(member.filename)
#         if not filename:
#             continue
#
#         # извлекаем ID
#         parts = filename.split("_")
#         if len(parts) < 3:
#             continue
#
#         try:
#             monument_id = int(parts[1])
#         except ValueError:
#             continue
#
#         # номер фото
#         photo_num = parts[2]
#
#         new_name = f"img_{monument_id}_{photo_num}.jpg"
#         target_path = IMG_DIR / new_name
#
#         with zip_ref.open(member) as source, open(target_path, "wb") as target:
#             shutil.copyfileobj(source, target)



def extract_monument_id(filename: str) -> int | None:
    """Создание mapping: id → фото"""
    name = Path(filename).stem
    parts = name.split("_")
    if len(parts) < 3:
        return None
    try:
        return int(parts[1])
    except ValueError:
        return None


image_map = defaultdict(list)
for fname in os.listdir(IMG_DIR):
    if not fname.lower().endswith((".jpg", ".jpeg", ".png")):
        continue
    monument_id = extract_monument_id(fname)
    if monument_id is None:
        continue
    image_map[monument_id].append(str(IMG_DIR / fname))


# Объединяем CSV + фото
merged = []
for _, row in df.iterrows():
    monument_id = int(row["id"])
    if monument_id not in image_map:
        continue
    for img_path in image_map[monument_id]:
        merged.append({
            "monument_id": monument_id,
            "name": row["name"],
            "address": row["address"],
            "style": row["style"],
            "year": row["year"],
            "architect": row["architect"],
            "description": row["text"] if pd.notna(row.get("text")) else "",
            "image_path": img_path
        })

print(f"Всего связок фото-памятник: {len(merged)}")

# Загрузка CLIP
device = "cuda" if torch.cuda.is_available() else "cpu"

model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(device)
processor = CLIPProcessor.from_pretrained(
    "openai/clip-vit-base-patch32",
    use_fast=True
)

model.eval()

def encode_image(image_path: str):
    image = Image.open(image_path).convert("RGB")

    inputs = processor(
        images=image,
        return_tensors="pt"
    )

    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        image_features = model.get_image_features(**inputs)
        image_features = image_features / image_features.norm(dim=-1, keepdim=True)

    return image_features.cpu().numpy()[0]

# Создание FAISS индекса
embeddings = []
metadata = []

for item in tqdm(merged, desc="Encoding images"):
    emb = encode_image(item["image_path"])
    embeddings.append(emb)
    metadata.append({
        "monument_id": item["monument_id"],
        "name": item["name"],
        "address": item["address"],
        "style": item["style"],
        "year": item["year"],
        "architect": item["architect"],
        "description": item.get("description", ""),
        "image_path": item["image_path"]
    })

embeddings = np.array(embeddings).astype("float32")
dim = embeddings.shape[1]

index = faiss.IndexFlatIP(dim)  # cosine similarity (векторы уже нормализованы)
index.add(embeddings)

# Сохраняем индекс и метаданные
FAISS_INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
faiss.write_index(index, str(FAISS_INDEX_PATH))

for path in (METADATA_PATH_CLIP, METADATA_PATH_ROOT):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

print(f"FAISS индекс сохранён: {FAISS_INDEX_PATH}")
print(f"Метаданные сохранены: {METADATA_PATH_CLIP}, {METADATA_PATH_ROOT}")
