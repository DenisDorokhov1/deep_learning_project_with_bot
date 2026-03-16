# 🏛 Telegram Bot: Monument Recognition with CLIP / DINO + RAG

Telegram-бот для распознавания архитектурных памятников Москвы по фотографии  
с использованием **визуальных моделей (CLIP / DINOv2)**,  
**FAISS-поиска** и **LLM-генерации текстового ответа**.

Бот принимает изображение памятника, определяет объект,  
извлекает информацию из датасета и формирует связное описание.

---

## Возможности

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
- Python 3.11
- python-telegram-bot
- logging

---

## Установка и запуск

После скачивания репозитория на свою локальную машину нужно:

### 1 Создать виртуальное окружение

```bash
python -m venv venv
source venv/bin/activate  # Linux / Mac
venv\Scripts\activate 
```

### 2 Установить зависимости
```bash
pip install -r requirements.txt
```
---

# Также нужно:
### Настройка отправки записей в Google Sheets

Чтобы бот автоматически сохранял жалобы пользователей в Google Таблицу, необходимо настроить доступ через Google Cloud Service Account.

---

#### 1. Создайте проект в Google Cloud

1. Перейдите в Google Cloud Console:  
   https://console.cloud.google.com/

2. Нажмите **Select project → New Project**

3. Создайте новый проект

Официальная документация:  
https://cloud.google.com/resource-manager/docs/creating-managing-projects

---

#### 2. Включите Google Sheets API

1. В Google Cloud Console откройте:  
   **APIs & Services → Library**

2. Найдите **Google Sheets API**

3. Нажмите **Enable**

Документация:  
https://developers.google.com/sheets/api/quickstart/python

---

#### 3. Создайте Service Account

1. Перейдите в:  
   **APIs & Services → Credentials**

2. Нажмите **Create Credentials → Service Account**

3. Укажите имя (например: `telegram-bot-sheets`)

4. Нажмите **Create and Continue**

5. Роль можно не назначать (или оставить Viewer)

6. Завершите создание

Документация:  
https://cloud.google.com/iam/docs/service-accounts-create

---

#### 4. Создайте JSON-ключ

1. Откройте созданный Service Account  
2. Перейдите во вкладку **Keys**  
3. Нажмите **Add Key → Create new key**  
4. Выберите формат **JSON**  
5. Скачайте файл  

Этот файл необходимо сохранить в проекте (в папке `/api`).

---

#### 5. Предоставьте доступ к Google Таблице

1. Создайте новую Google Таблицу  
2. Откройте её  
3. Нажмите **Поделиться**  
4. Вставьте email Service Account  

Email выглядит примерно так:

``` telegram-bot-sheets@your-project-id.iam.gserviceaccount.com```


5. Дайте права **Editor**

**Без этого бот не сможет записывать данные.**

---

#### 6. Получите ID таблицы

ID — это часть URL:

```https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit#gid=0```


Скопируйте `SPREADSHEET_ID`.

---

### Настройка переменных окружения

Создайте файл `.env` в корне проекта:

```env
BOT_TOKEN=your_telegram_bot_token
OPENAI_API_KEY=your_openai_api_key
SERVICE_ACCOUNT_FILE=path/to/your/service_account.json
SPREADSHEET_ID=your_spreadsheet_id
```
# Где получить ключи
- **Telegram Bot Token**
Создать бота через @BotFather в Telegram.
Инструкция:
https://core.telegram.org/bots#creating-a-new-bot

- **OpenAI API Key**
Создать ключ в личном кабинете:
https://platform.openai.com/api-keys

-------------

## Проверка работы
После запуска бот должен:
- Принять жалобу
- Добавить новую строку в Google Таблицу
- Сохранить:
```
user_id
username
текст жалобы
дату
```

В странах с ограничением OpenAI требуется VPN.

## Скачать full_dataset.csv можно вот [тут](https://drive.google.com/file/d/1VtO5RhNFSBKGVyhrk6viVHiXIzNJfwHw/view?usp=drive_link)
Нужно поместить его в папку  `/data `

## Скачать zip со всеми фото можно [тут](https://drive.google.com/file/d/1OLuv1ck21_NDG34XvwvWXkOcw1t8bHWC/view?usp=drive_link)
Их нужно разархивировать, создать папку  `/images` в корне проекта и вставить все фото туда
## Сборка FAISS-индексов

Перед первым запуском бота необходимо построить индексы. Порядок: сначала CLIP, затем DINO (DINO использует metadata от CLIP).

```bash
# CLIP — создаёт data/clip_data/monuments.faiss и monuments_metadata.json
python scripts/build/build_clip_faiss.py

# DINO — создаёт data/dino/monuments_dino.faiss и index_map_dino.json
python scripts/build/build_dino_faiss.py
```
### Еще раз важно: 

Требуются: директория `images/` с фотографиями и `data/full_dataset.csv`.

---

## Запуск бота

Запуск через один из двух скриптов:

- `bot_clip.py` — модель CLIP
- `bot_dino.py` — модель DINO