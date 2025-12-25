import faiss
import json
from scripts.clip_model import encode_image
from scripts.config import FAISS_INDEX_PATH, METADATA_PATH, TOP_K

# Загружаем ОДИН РАЗ
index = faiss.read_index(FAISS_INDEX_PATH)

with open(METADATA_PATH, "r", encoding="utf-8") as f:
    metadata = json.load(f)

def search_monument(image_path: str):
    query_emb = encode_image(image_path)

    D, I = index.search(query_emb, TOP_K)

    results = []
    for score, idx in zip(D[0], I[0]):
        item = metadata[idx]
        results.append({
            "score": float(score),
            **item
        })

    return results
