from aiogram import types
from aiogram.dispatcher.filters import Command
from app import session
from keyboards.inline.questions import question_keyboard, answer_keyboard
from loader import dp, bot
from models.question import Question


@dp.message_handler(Command("questions"))
async def begin_questions(message: types.Message):
    text = "Для начала выберите направление, которое вам интересно!"
    q_keyboard = await question_keyboard(messages='questions')
    await bot.send_message(message.from_user.id, text=text, reply_markup=q_keyboard)


idx = 1
course_id = None


@dp.callback_query_handler()
async def answer_questions_1(call: types.CallbackQuery):
    global course_id
    global idx
    if 'answer' in call.data:
        idx += 1
        await display_question(call, course_id, idx)
        return
    if 'course' in call.data:
        idx = 1
        course_id = int(call.data[6])
        await display_question(call, course_id, idx)


async def display_question(call, course_id, question_number):
    questions_counter = count_questions(course_id)
    if question_number == questions_counter:
        await bot.send_message(call.from_user.id,
                               f"По результатам опроса Вам рекомендован следующий курс:\n{course_id + 1}",
                               parse_mode='MARKDOWN')
        return
    question = get_question(course_id, question_number)
    if question is None:
        await bot.send_message(call.from_user.id, "Ошибка при выборе вопроса")

    a_keyboard = answer_keyboard(messages='answer', answer_data=question.answers)
    await bot.send_message(call.from_user.id, f"*Вопрос № {question.number}:*\n{question.name}",
                           reply_markup=a_keyboard,
                           parse_mode='MARKDOWN', )


def get_question(course_id, number):
    try:
        return session.query(Question).filter(Question.course_id == course_id, Question.number == number).one()
    except Exception:
        return None


def count_questions(course_id):
    return session.query(Question).filter(Question.course_id == course_id).count()
