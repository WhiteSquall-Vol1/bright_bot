from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import ContentType
from aiogram import types
from data.config import support_ids
from keyboards.inline.adminkeyboard import update_courses, admin_keyboard
from loader import bot, dp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    user_id = message.from_user.id
    if user_id in support_ids:
        admins_keyboard = await admin_keyboard(messages="admincommands")
        await dp.bot.send_message(user_id, "⚠️Ожидайте запроса на поддержку от пользователя.\n\n"
                                           "⚠️Для загрузки и обновления курсов - прикрепите файл EXCEL в чат с ботом",
                                  reply_markup=admins_keyboard)
    else:
        await message.answer(f"*Привет, {message.from_user.full_name}!*\n\n"
                         f"_Чтобы подобрать нужный для Вас курс пройдите в пункт меню_ *'Вопросы'*\n\n"
                         f"Спасибо!", parse_mode="MARKDOWN")


@dp.callback_query_handler(text='addc')
async def send_to_support_call(call: types.CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    if user_id != support_ids:
        return
    await call.message.edit_text("Вставьте файл в чат для обновления курсов")
    await state.set_state("addcourses")


@dp.message_handler(state="addcourses", content_types=ContentType.DOCUMENT)
async def doc_handler(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if user_id != support_ids:
        return
    try:
        await message.document.download('data/botquest.xlsx')
        await bot.send_message(message.from_user.id, "База кусров обновлена!")
        await update_courses(user_id)
    except Exception:
        await bot.send_message(message.from_user.id, "Что-то пошло не так")
    await state.reset_state()


@dp.callback_query_handler(text='delc')
async def send_to_support_call(call: types.CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    if user_id != support_ids:
        return
    await bot.send_message(user_id, "Кнопка удаления сработала!")
    #delcourses_keyboard = allcourses
    #await call.message.edit_text(f"Выберите какой курс вы хотите удалить: {courses}", reply_markup=delcourses_keyboard)
    await state.set_state("delcourses")


@dp.message_handler(state="delcourses")
async def doc_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id != support_ids:
        return
    try:
        await bot.send_message(user_id, "Курс удален!")
    except Exception:
        await bot.send_message(user_id, "Что-то пошло не так, курс не удален!")

