from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from keyboards.inline.users import start_ikb
from keyboards.inline.users.general import UserCallbackData
from aiogram import F, Router
from aiogram.types import Message, FSInputFile
from models import User
import os

user_start_router = Router(name='user_start')


@user_start_router.message(F.text == '/start')
async def command_start(message: Message):
    await message.delete()
    if await User.get(pk=message.from_user.id):

        filename = fr"photos/bot.png"

        await message.answer_photo(
            photo=FSInputFile(filename),
            caption=os.getenv('TEXT'),
            reply_markup=await start_ikb()
        )

    else:
        user = User(id=message.from_user.id, name=message.from_user.full_name, username=f'@{message.from_user.username}')
        await user.save()

        filename = fr"photos/bot.png"

        await message.answer_photo(
            photo=FSInputFile(filename),
            caption=os.getenv('TEXT'),
            reply_markup=await start_ikb()
        )


@user_start_router.callback_query(UserCallbackData.filter(F.action == 'all'))
async def start_panel_2(callback: CallbackQuery):
    await callback.message.edit_text(
        text='Выберите один из предложенных вариантов:',
        reply_markup=await start_ikb()



    )

