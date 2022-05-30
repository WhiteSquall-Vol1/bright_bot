from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Запустить бота"),
        types.BotCommand("questions", "Подобрать курс по вопросам"),
        types.BotCommand("support_call", "Обратиться в поддержку"),
    ])
