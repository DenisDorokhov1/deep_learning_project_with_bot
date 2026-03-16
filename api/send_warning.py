from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from datetime import datetime
from scripts.config import SPREADSHEET_ID, SERVICE_ACCOUNT_FILE

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# АВТОРИЗАЦИЯ (создаётся один раз)
credentials = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=SCOPES
)

service = build("sheets", "v4", credentials=credentials)
sheet = service.spreadsheets()


def create_headers_if_not_exist():
    """СОЗДАНИЕ ЗАГОЛОВКОВ"""
    headers = [
        ["id", "user_id", "user_message", "message_time"]
    ]

    sheet.values().update(
        spreadsheetId=SPREADSHEET_ID,
        range="Лист1!A1:D1",
        valueInputOption="RAW",
        body={"values": headers}
    ).execute()


def append_feedback(user_id: int, message: str):
    """ДОБАВЛЕНИЕ FEEDBACK"""
    # Получаем текущее количество строк
    result = sheet.values().get(
        spreadsheetId=SPREADSHEET_ID,
        range="Лист1!A:A"
    ).execute()

    values = result.get("values", [])
    next_id = len(values)  # автоинкремент по количеству строк

    row = [
        next_id,
        user_id,
        message,
        str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    ]

    sheet.values().append(
        spreadsheetId=SPREADSHEET_ID,
        range="Лист1!A:D",
        valueInputOption="RAW",
        insertDataOption="INSERT_ROWS",
        body={"values": [row]}
    ).execute()
