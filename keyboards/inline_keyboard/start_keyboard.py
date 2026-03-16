from telegram import InlineKeyboardMarkup, InlineKeyboardButton

start_inline_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Распознать памятник",
                callback_data="recognize_monument"
            )
        ]
    ]
)
