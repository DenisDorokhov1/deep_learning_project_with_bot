import os
from telegram import Update
from telegram.ext import ContextTypes

from scripts.faiss_search_dino import search_monument
from scripts.llm.generate import generate_monument_text
from scripts.formatter import format_answer
from scripts.config import CONFIDENCE_THRESHOLD
from scripts.logger import logger


TEMP_IMAGE = "user_photo.jpg"

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        photo = update.message.photo[-1]
        file = await context.bot.get_file(photo.file_id)
        await file.download_to_drive(TEMP_IMAGE)

        results = search_monument(TEMP_IMAGE)

        if not results or results[0]["score"] < CONFIDENCE_THRESHOLD:
            await update.message.reply_text(
                "😕 Не удалось уверенно определить здание (DINO)."
            )
            return

        top = results[0]

        text = generate_monument_text(top)
        await update.message.reply_text(text)

        logger.info(
            f'model=DINO | monument="{top["name"]}" | score={top["score"]:.4f}'
        )

    finally:
        if os.path.exists(TEMP_IMAGE):
            os.remove(TEMP_IMAGE)
