from telegram import InlineKeyboardButton, InlineKeyboardMarkup

error_inline_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Сообщите о неполадках тут",
                callback_data="report_issue"
            )
        ]
    ]
)
