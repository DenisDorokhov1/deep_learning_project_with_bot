import sys
import os
import json
import numpy as np
import faiss
from pathlib import Path
from tqdm import tqdm

# Корень проекта — для корректного импорта и путей при запуске из scripts/build/
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.dino_model import encode_image


# Пути
BASE_METADATA_PATH = PROJECT_ROOT / "data" / "clip_data" / "monuments_metadata.json"
DINO_DIR = PROJECT_ROOT / "data" / "dino"
FAISS_PATH = DINO_DIR / "monuments_dino.faiss"
INDEX_MAP_PATH = DINO_DIR / "index_map_dino.json"

DINO_DIR.mkdir(parents=True, exist_ok=True)

# Загружаем БАЗОВЫЙ metadata (создаётся build_clip_faiss.py)
with open(BASE_METADATA_PATH, "r", encoding="utf-8") as f:
    base_metadata = json.load(f)

embeddings = []
index_map = []   # FAISS index → index в base_metadata

# Кодирование изображений
for idx, item in enumerate(tqdm(base_metadata, desc="Encoding images with DINOv2")):
    img_path = item.get("image_path")
    if not img_path:
        continue

    # Поддержка абсолютных и относительных путей
    full_path = Path(img_path) if Path(img_path).is_absolute() else PROJECT_ROOT / img_path
    if not full_path.exists():
        continue

    try:
        emb = encode_image(str(full_path))
        embeddings.append(emb)
        index_map.append(idx)  # ← связь с base_metadata
    except Exception as e:
        print(f"Ошибка с файлом {img_path}: {e}")

# Создание FAISS
embeddings = np.array(embeddings, dtype="float32")

dim = embeddings.shape[1]
index = faiss.IndexFlatIP(dim)
index.add(embeddings)

faiss.write_index(index, str(FAISS_PATH))

# Сохраняем index_map
with open(INDEX_MAP_PATH, "w", encoding="utf-8") as f:
    json.dump(index_map, f, indent=2)

print("DINOv2 FAISS индекс создан:", FAISS_PATH)
print("index_map сохранён:", INDEX_MAP_PATH)
print(f" Всего векторов: {len(index_map)}")
