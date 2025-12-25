import json
import faiss
import numpy as np
from scripts.dino_model import encode_image

FAISS_PATH = "data/dino/monuments_dino.faiss"
INDEX_MAP_PATH = "data/dino/index_map_dino.json"
METADATA_PATH = "data/monuments_metadata.json"

# -----------------------------
# Загрузка при старте
# -----------------------------
index = faiss.read_index(FAISS_PATH)

with open(INDEX_MAP_PATH, "r", encoding="utf-8") as f:
    index_map = json.load(f)

with open(METADATA_PATH, "r", encoding="utf-8") as f:
    metadata = json.load(f)


def search_monument(image_path: str, top_k=3):
    # 1. DINO embedding (одно изображение)
    emb = encode_image(image_path)
    emb = np.array([emb], dtype="float32")

    # 2. FAISS search
    scores, indices = index.search(emb, top_k)

    results = []
    for faiss_idx, score in zip(indices[0], scores[0]):
        meta_idx = index_map[faiss_idx]
        item = metadata[meta_idx]

        results.append({
            "score": float(score),
            **item
        })

    return results
