import datetime
import pandas as pandas
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from app import session
from loader import bot
from models.answer import Answer
from models.course import Course
from models.question import Question


adminkeyboard_callback = CallbackData('messages')


async def admin_keyboard(messages):
    if messages == 'admincommands':
        buttons = [[InlineKeyboardButton(text="Добавить курс", callback_data='addc'),
                   InlineKeyboardButton(text="Удалить курс", callback_data='delc')]]
        ad_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
        return ad_keyboard


async def update_courses(user_id):
    try:
        data = pandas.read_excel("data/botquest.xlsx", sheet_name='data', usecols=['courses', 'questions', 'answers'], )
    except Exception:
        await bot.send_message(user_id, "Не получилось")
    courses_array = []
    questions_array = []
    courses = data['courses']
    questions = data['questions']
    answers = data['answers']
    created = datetime.datetime.now()
    for course in courses:
        if type(course) is str and len(course) > 0:
            courses_array.append(insert_or_update_course(course, created))

    course_idx = 0
    for idx, question in enumerate(questions):
        if type(question) is str and len(question) > 0:
            questions_array.append(insert_or_update_question(courses_array[course_idx], question, created, idx))
        if question == '*':
            course_idx += 1

    question_idx = 0
    for idx, answer in enumerate(answers):
        if type(answers) is str and len(answers) > 0:
            insert_or_update_answer(questions_array[question_idx], answer, created, idx)
        if answer == '*':
            question_idx += 1

    await bot.send_message(user_id, "Получилось")


def insert_or_update_course(name, created):
    course_count = session.query(Course).filter(Course.name == name).count()
    if course_count > 0:
        return
    course = Course(name=name, created=created)
    session.add(course)
    session.commit()
    return course.id


def insert_or_update_question(course_id, name, created, idx):
    questions = session.query(Question).filter(Question.course_id == course_id)
    question = None
    if len(questions) > 0:
        question = questions[idx]
        question.name = name
    else:
        question = Question(name=name, number=idx, created=created, course_id=course_id)

    session.add(question)
    session.commit()
    return question.id


def insert_or_update_answer(question_id, name, created, idx):
    answers = session.query(Answer).filter(Answer.question_id == question_id)
    answer = None
    if len(answers) > 0:
        answer = answers[idx]
        answer.name = name
    else:
        answer = Answer(name=name, created=created, question_id=question_id)

    session.add(answer)
    session.commit()
    return answer.id
