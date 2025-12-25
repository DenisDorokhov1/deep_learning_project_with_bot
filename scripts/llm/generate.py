from scripts.llm.client import client
from scripts.llm.prompt import SYSTEM_PROMPT

def generate_monument_text(monument: dict) -> str:
    """
    monument — это результат FAISS:
    {
        "name": "...",
        "address": "...",
        "year": "...",
        "architect": "...",
        "style": "...",
        "description": "...",
        "score": 0.95
    }
    """

    user_prompt = f"""
Название: {monument.get("name")}
Адрес: {monument.get("address")}
Год постройки: {monument.get("year")}
Архитектор: {monument.get("architect")}
Архитектурный стиль: {monument.get("style")}
Описание из базы: {monument.get("description")}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",  # или gpt-3.5
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.6,
        max_tokens=300,
    )

    return response.choices[0].message.content.strip()
