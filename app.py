from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats


async def on_startup(bot: Bot):
    await bot.set_my_commands(
        commands=[
            BotCommand(command='/start', description='Restart'),
            BotCommand(command='/admin', description='Admin panel'),
        ],
        scope=BotCommandScopeAllPrivateChats(),
        language_code='ru'
    )


if __name__ == '__main__':
    from loader import dp, bot
    from handlers import router

    dp.include_router(router=router)
    dp.startup.register(on_startup)
    dp.run_polling(bot)

