from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CommandHandler,
    CallbackQueryHandler,
    filters
)
from api.send_warning import create_headers_if_not_exist
from handlers.commands import start, help_command
from handlers.photos_clip import handle_photo
from handlers.fallback import handle_text
from handlers.callbacks import recognize_callback, report_issue_callback, feedback_message_handler
from scripts.config import BOT_TOKEN

create_headers_if_not_exist()

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CallbackQueryHandler(recognize_callback, pattern="^recognize_monument$"))
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))


    # app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(
        CallbackQueryHandler(report_issue_callback, pattern="report_issue")
    )

    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, feedback_message_handler)
    )
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    print("🤖 CLIP-бот запущен")
    app.run_polling()

if __name__ == "__main__":
    main()
