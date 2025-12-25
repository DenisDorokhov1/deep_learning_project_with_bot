import os
import zipfile
import shutil
import pandas as pd
from collections import defaultdict
from PIL import Image
import numpy as np
from tqdm import tqdm
import faiss
import clip
import torch
import json

# -------------------------------
# Параметры
# -------------------------------
CSV_PATH = "data/full_dataset.csv"
ZIP_PATH = "images.zip"
IMG_DIR = "images"
FAISS_INDEX_PATH = "data/clip_data/monuments.faiss"
METADATA_PATH = "data/clip_data/monuments_metadata.json"

# -------------------------------
# 1. Загрузка CSV
# -------------------------------
df = pd.read_csv(CSV_PATH)

# -------------------------------
# 2. Распаковка ZIP с фото
# -------------------------------
# os.makedirs("images", exist_ok=True)
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
#         target_path = os.path.join("images", new_name)
#
#         with zip_ref.open(member) as source, open(target_path, "wb") as target:
#             shutil.copyfileobj(source, target)

# -------------------------------
# 3. Создание mapping: id → фото
# -------------------------------
def extract_monument_id(filename: str) -> int | None:
    name = os.path.splitext(filename)[0]
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
    image_map[monument_id].append(os.path.join(IMG_DIR, fname))

# -------------------------------
# 4. Объединяем CSV + фото
# -------------------------------
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
            "image_path": img_path
        })

print(f"Всего связок фото → памятник: {len(merged)}")

# -------------------------------
# 5. Загрузка CLIP
# -------------------------------
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)
model.eval()

def encode_image(image_path: str):
    image = Image.open(image_path).convert("RGB")
    image_input = preprocess(image).unsqueeze(0).to(device)
    with torch.no_grad():
        embedding = model.encode_image(image_input)
        embedding = embedding / embedding.norm(dim=-1, keepdim=True)
    return embedding.cpu().numpy()[0]

# -------------------------------
# 6. Создание FAISS индекса
# -------------------------------
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
        "image_path": item["image_path"]
    })

embeddings = np.array(embeddings).astype("float32")
dim = embeddings.shape[1]

index = faiss.IndexFlatIP(dim)  # cosine similarity (векторы уже нормализованы)
index.add(embeddings)

# -------------------------------
# 7. Сохраняем индекс и метаданные
# -------------------------------
faiss.write_index(index, FAISS_INDEX_PATH)

with open(METADATA_PATH, "w", encoding="utf-8") as f:
    json.dump(metadata, f, ensure_ascii=False, indent=2)

print(f"FAISS индекс сохранён: {FAISS_INDEX_PATH}")
print(f"Метаданные сохранены: {METADATA_PATH}")
