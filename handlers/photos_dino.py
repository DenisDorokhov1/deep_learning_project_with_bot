import os
from telegram import Update
from telegram.ext import ContextTypes

from scripts.faiss_search_dino import search_monument
from scripts.llm.generate import generate_monument_text
from keyboards.inline_keyboard.error_button import error_inline_keyboard
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
                "Не удалось уверенно определить здание (DINO)."
            )
            return

        top = results[0]

        text = generate_monument_text(top)

        logger.info(
            f'model=DINO | monument="{top["name"]}" | score={top["score"]:.4f}'
        )

        await update.message.reply_text(
            text,
            reply_markup=error_inline_keyboard
        )

    finally:
        if os.path.exists(TEMP_IMAGE):
            os.remove(TEMP_IMAGE)
