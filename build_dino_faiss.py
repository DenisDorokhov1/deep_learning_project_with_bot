import os
import json
import numpy as np
import faiss
from tqdm import tqdm
from scripts.dino_model import encode_image

# -----------------------------
# Пути
# -----------------------------
BASE_METADATA_PATH = "data/clip_data/monuments_metadata.json"
DINO_DIR = "data/dino"
FAISS_PATH = os.path.join(DINO_DIR, "monuments_dino.faiss")
INDEX_MAP_PATH = os.path.join(DINO_DIR, "index_map_dino.json")

os.makedirs(DINO_DIR, exist_ok=True)

# -----------------------------
# Загружаем БАЗОВЫЙ metadata
# -----------------------------
with open(BASE_METADATA_PATH, "r", encoding="utf-8") as f:
    base_metadata = json.load(f)

embeddings = []
index_map = []   # FAISS index → index в base_metadata

# -----------------------------
# Кодирование изображений
# -----------------------------
for idx, item in enumerate(tqdm(base_metadata, desc="Encoding images with DINOv2")):
    img_path = item.get("image_path")

    if not img_path or not os.path.exists(img_path):
        continue

    try:
        emb = encode_image(img_path)
        embeddings.append(emb)
        index_map.append(idx)  # ← связь с base_metadata
    except Exception as e:
        print(f"Ошибка с файлом {img_path}: {e}")

# -----------------------------
# Создание FAISS
# -----------------------------
embeddings = np.array(embeddings, dtype="float32")

dim = embeddings.shape[1]
index = faiss.IndexFlatIP(dim)
index.add(embeddings)

faiss.write_index(index, FAISS_PATH)

# -----------------------------
# Сохраняем index_map
# -----------------------------
with open(INDEX_MAP_PATH, "w", encoding="utf-8") as f:
    json.dump(index_map, f, indent=2)

print("✅ DINOv2 FAISS индекс создан:", FAISS_PATH)
print("✅ index_map сохранён:", INDEX_MAP_PATH)
print(f"📊 Всего векторов: {len(index_map)}")
