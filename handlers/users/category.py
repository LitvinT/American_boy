from datetime import datetime

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message
from keyboards.inline.users import category_ikb
from keyboards.inline.users.general import UserCallbackData


user_category_router = Router(name='user_category')


class Category(StatesGroup):
    star = State()
    thanks = State()


@user_category_router.callback_query(UserCallbackData.filter((F.target == 'category') & (F.action == 'get')))
async def paginate_categories(callback: CallbackQuery, callback_data: UserCallbackData, state: FSMContext) -> None:

    if callback_data.calculator_id == 3:
        await callback.message.edit_text(
            text='Выберите один из предложенных вариантов',
            reply_markup=await category_ikb()
        )
