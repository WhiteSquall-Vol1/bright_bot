from aiogram import executor
import sqlalchemy as db
from sqlalchemy.orm import declarative_base, sessionmaker
import middlewares, filters, handlers
from loader import dp
from utils.misc.set_bot_commands import set_default_commands
from utils.notify_admins import on_startup_notify

engine = db.create_engine(f"sqlite:///bright.db")
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()
Base = declarative_base()


async def on_startup(dispatcher):
    await set_default_commands(dispatcher)
    await on_startup_notify(dispatcher)

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
