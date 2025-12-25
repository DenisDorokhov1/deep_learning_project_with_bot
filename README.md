# 🏛 Telegram Bot: Monument Recognition with CLIP / DINO + RAG

Telegram-бот для распознавания архитектурных памятников Москвы по фотографии  
с использованием **визуальных моделей (CLIP / DINOv2)**,  
**FAISS-поиска** и **LLM-генерации текстового ответа**.

Бот принимает изображение памятника, определяет объект,  
извлекает информацию из датасета и формирует связное описание.

---

## 🚀 Возможности

-  Распознавание памятников по фото
-  Две визуальные модели:
  - CLIP
  - DINOv2
-  Поиск по векторной базе FAISS
-  Генерация описаний с помощью OpenAI API
-  Логирование распознаваний (название + уверенность)
-  Telegram inline-интерфейс

---

## Что использовали

### Computer Vision
- CLIP
- DINOv2
- FAISS

### LLM
- OpenAI API (Chat Completions)
- RAG-подход (FAISS + LLM)

### Backend
- Python 3.10+
- python-telegram-bot
- logging

---

## Установка и запуск

### 1 Клонировать репозиторий
```bash
git clone https://github.com/your-username/monument-bot.git
cd monument-bot
```

### 2 Создать виртуальное окружение

```bash
python -m venv venv
source venv/bin/activate  # Linux / Mac
venv\Scripts\activate 
```

### 3 Установить зависимости
```bash
pip install -r requirements.txt
```
---

## Установка переменных окружения
Создай файл .env или задай переменные вручную:
```
BOT_TOKEN=your_telegram_bot_token
OPENAI_API_KEY=your_openai_key
```
 В странах с ограничением OpenAI требуется VPN.


## Запуск бота происходит через запуск одного из двух скриптов
- bot_clip.py - модель CLIP 
- bot_dino.py - модель DINO