import os

from aiogram import F, Router
from aiogram.types import Message, FSInputFile

from keyboards.inline.users import start_ikb
from models import User

user_start_router = Router(name='user_start')


@user_start_router.message(F.text == '/start')
async def command_start(message: Message):
    await message.delete()
    if await User.get(pk=message.from_user.id):

        filename = fr"photos/bot.png"

        await message.answer_photo(
            photo=FSInputFile(filename),
            caption='👋 Hello, We are Interhash company! '
                 'We are engaged in providing complex services for mining. '
                 'We have been on the market since 2017 and are the official representatives of the ViaBTC mining pool '
                 'in Eastern Europe and CIS countries.',
            reply_markup=await start_ikb()
        )

    else:
        user = User(id=message.from_user.id, name=message.from_user.full_name,
                    username=f'@{message.from_user.username}')
        await user.save()

        filename = fr"photos/bot.png"

        await message.answer_photo(
            photo=FSInputFile(filename),
            caption='👋 Hello, We are Interhash company! '
                 'We are engaged in providing complex services for mining. '
                 'We have been on the market since 2017 and are the official representatives of the ViaBTC mining pool '
                 'in Eastern Europe and CIS countries.',
            reply_markup=await start_ikb()
        )
