from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from app import session
from models.course import Course

question_callback = CallbackData('qmenu', 'messages')
answer_callback = CallbackData('answer', 'messages')


async def question_keyboard(messages):
    if messages == 'questions':
        cources = session.query(Course).all()
        buttons = []
        for item in cources:
            buttons.append([InlineKeyboardButton(text=item.name, callback_data=f'course{item.id}')])
        q_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
        return q_keyboard


def answer_keyboard(messages, answer_data):
    if messages == 'answer':
        a_keyboard = InlineKeyboardMarkup()
        answers = []
        for item in answer_data:
            answers.append(InlineKeyboardButton(text=item.name, callback_data=f'answer{item.id}'))

        a_keyboard.row(
            *answers
        )
        return a_keyboard