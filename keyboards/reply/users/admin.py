from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin_panel = ReplyKeyboardMarkup(
    one_time_keyboard=False,
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(
                text='Check users🥳'
            )
        ],
    ]
)
