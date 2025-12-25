import os
from dotenv import load_dotenv
from pathlib import Path

# Получаем путь к корню проекта (относительно scripts/config.py)
BASE_DIR = Path(__file__).resolve().parent.parent  # поднимаемся на два уровня до PythonProject2
ENV_PATH = BASE_DIR / ".env"

# Загружаем переменные из .env
load_dotenv(dotenv_path=ENV_PATH)

# Получаем токен
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not BOT_TOKEN:
    raise ValueError("Не найден токен бота в .env")
if not OPENAI_API_KEY:
    raise ValueError("Не найден openai key в .env")


FAISS_INDEX_PATH = "data/clip_data/monuments.faiss"
METADATA_PATH = "data/monuments_metadata.json"

CONFIDENCE_THRESHOLD = 0.60  # можно подкрутить
TOP_K = 3


