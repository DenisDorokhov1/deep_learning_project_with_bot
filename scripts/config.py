import os
from dotenv import load_dotenv
from pathlib import Path

# Получаем путь к корню проекта (относительно scripts/config.py)
BASE_DIR = Path(__file__).resolve().parent.parent  # поднимаемся на два уровня до sightseeing_bot
ENV_PATH = BASE_DIR / ".env"

# Загружаем переменные из .env
load_dotenv(dotenv_path=ENV_PATH)

# Получаем токен
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERVICE_ACCOUNT_FILE = os.getenv("SERVICE_ACCOUNT_FILE")
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")

if not BOT_TOKEN:
    raise ValueError("Не найден токен бота в .env")
if not OPENAI_API_KEY:
    raise ValueError("Не найден openai key в .env")


# Пути к данным (относительно корня проекта)
FAISS_INDEX_PATH = str(BASE_DIR / "data" / "clip_data" / "monuments.faiss")
METADATA_PATH = str(BASE_DIR / "data" / "monuments_metadata.json")
FAISS_DINO_PATH = str(BASE_DIR / "data" / "dino" / "monuments_dino.faiss")
INDEX_MAP_DINO_PATH = str(BASE_DIR / "data" / "dino" / "index_map_dino.json")

CONFIDENCE_THRESHOLD = 0.60  # можно подкрутить
TOP_K = 3


