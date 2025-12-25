from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CommandHandler,
    CallbackQueryHandler,
    filters
)

from handlers.commands import start, help_command
from handlers.callbacks import recognize_callback
from handlers.photos_clip import handle_photo
from handlers.fallback import handle_text
from scripts.config import BOT_TOKEN

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CallbackQueryHandler(recognize_callback, pattern="^recognize_monument$"))
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("🤖 CLIP-бот запущен")
    app.run_polling()

if __name__ == "__main__":
    main()
