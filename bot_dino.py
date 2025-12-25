from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

from handlers.commands import start, help_command
from handlers.callbacks import recognize_callback
from handlers.photos_dino import handle_photo
from handlers.fallback import handle_text

from scripts.config import BOT_TOKEN


TEMP_IMAGE = "user_photo.jpg"


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Команды
    app.add_handler(CallbackQueryHandler(
        recognize_callback,
        pattern="^recognize_monument$"
    ))
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    # Фото
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    # Любой текст, который не команда и не фото
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("🤖 Бот запущен")
    app.run_polling()

if __name__ == "__main__":
    main()
