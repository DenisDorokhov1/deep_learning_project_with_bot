from telegram import Update
from telegram.ext import ContextTypes

async def recognize_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await query.message.reply_text(
        "📷 Отправь фотографию здания для распознавания"
    )
