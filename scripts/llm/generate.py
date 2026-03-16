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

    description = monument.get("description") or monument.get("text") or ""
    user_prompt = f"""
Название: {monument.get("name")}
Адрес: {monument.get("address")}
Год постройки: {monument.get("year")}
Архитектор: {monument.get("architect")}
Архитектурный стиль: {monument.get("style")}
Описание из базы: {description}
"""

    response = client.chat.completions.create(
        model="gpt-5-nano",  # или gpt-3.5
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ]
    )
    # response = client.responses.create(
    #     model="gpt-5-nano",  # или gpt-3.5
    #     input=SYSTEM_PROMPT + user_prompt,
    #     store=True
    # )
    return response.choices[0].message.content.strip()
