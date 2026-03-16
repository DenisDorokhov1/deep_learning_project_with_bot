from telegram import Update
from telegram.ext import ContextTypes
from api.send_warning import append_feedback

async def recognize_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await query.message.reply_text(
        "📷 Отправь фотографию здания для распознавания"
    )

async def report_issue_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Переводим пользователя в режим ввода сообщения
    context.user_data["awaiting_feedback"] = True

    await query.message.reply_text(
        "Пожалуйста, опишите проблему или неточность:"
    )


async def feedback_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Проверяем, ждём ли мы feedback
    if not context.user_data.get("awaiting_feedback"):
        return

    feedback_text = update.message.text
    user_id = update.effective_user.id

    # Сбрасываем режим
    context.user_data["awaiting_feedback"] = False

    try:
        append_feedback(user_id=user_id, message=feedback_text)

        await update.message.reply_text(
            "Спасибо! Сообщение сохранено."
        )

    except Exception as e:
        print("Google Sheets Error:", e)

        await update.message.reply_text(
            "⚠️ Произошла ошибка при сохранении сообщения."
        )