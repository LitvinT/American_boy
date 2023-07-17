from itertools import zip_longest

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from models import Coin
from .general import UserCallbackData


async def coin_ikb() -> InlineKeyboardMarkup:
    coins = await Coin.all(is_published=True)
    coin_iter = iter(coins)
    coin_iter = map(list, zip_longest(*([coin_iter]*2)))
    buttons = [
        [
            InlineKeyboardButton(
                text=coin.name.upper(),
                callback_data=UserCallbackData(
                    target='coins',
                    action='get',
                    coin_id=coin.id
                ).pack()
            )
            for coin in line
            if coin
        ]
        for line in coin_iter
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
