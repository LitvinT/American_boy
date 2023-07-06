from itertools import zip_longest

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from models import Calculator
from .general import UserCallbackData


async def start_ikb() -> InlineKeyboardMarkup:
    calculators = await Calculator.all(is_published=True)
    calculator_iter = iter(calculators)
    calculator_iter = map(list, zip_longest(*([calculator_iter]*1)))
    buttons = [
        [
            InlineKeyboardButton(
                text=calculator.name.upper(),
                callback_data=UserCallbackData(
                    target='category',
                    action='get',
                    calculator_id=calculator.id
                ).pack()
            )
            for calculator in line
            if calculator
        ]
        for line in calculator_iter
    ]
    # print(buttons)
    return InlineKeyboardMarkup(inline_keyboard=buttons)
