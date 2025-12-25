from telegram import Update
from telegram.ext import ContextTypes

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📸 Пожалуйста, отправь фотографию памятника.\n"
        "Для помощи напиши /help."
    )
