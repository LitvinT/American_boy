from aiogram.filters.callback_data import CallbackData


class UserCallbackData(CallbackData, prefix='user'):
    target: str
    action: str
    coin_id: int = None
    calculator_id: int = None
