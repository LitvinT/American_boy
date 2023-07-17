from aiogram import F, Router
from aiogram.types import Message

from keyboards.reply.users import admin, password
from models import Admin

user_password_router = Router(name='user_password_router')


@user_password_router.message(F.text == '/admin')
async def get_text_message(message: Message):
    await message.answer('Hi, put the button', reply_markup=password.pass_panel)


@user_password_router.message(F.text == 'Who are you?')
async def proporty(message: Message):
    await message.delete()
    if await Admin.get(pk=message.from_user.id):
        await message.answer(text=f'Hi, {message.from_user.full_name}😎', reply_markup=admin.admin_panel)
    else:
        await message.answer(text='Access denied')
