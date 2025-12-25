from telegram import Update
from telegram.ext import ContextTypes
from keyboards.start_keyboard import start_inline_keyboard

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! 👋\n\n"
        "Я могу определить архитектурный памятник по фото.\n"
        "Нажми кнопку ниже 👇",
        reply_markup=start_inline_keyboard
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📌 Как пользоваться ботом:\n\n"
        "1. Отправь фотографию памятника Москвы.\n"
        "2. Я постараюсь определить, что на фото.\n"
        "3. Если не получилось — попробуй другой ракурс.\n\n"
        "Просто отправь изображение."
    )
