from aiogram import Router, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile, ChatJoinRequest, ReplyKeyboardRemove
from tgbot.keyboards.inline import keyboard
from tgbot.keyboards import reply
import time
import sqlite3
import os

con = sqlite3.connect("db_SQLite.db")
cursor = con.cursor()

user_router = Router()


@user_router.message(CommandStart())
async def user_start(message: Message, bot: Bot):
    print(message.from_user.id)
    text_start = cursor.execute("SELECT text_start FROM text_command where id=1;").fetchone()[0]
    print(text_start)
    # text_start_values = ', '.join(item[0] for item in text_start)
    await message.answer(f"{text_start}")

@user_router.chat_join_request()
async def chat_join_request(join_request: ChatJoinRequest, bot: Bot):
    # text_join1 = cursor.execute("SELECT text_join FROM main.text_command;").fetchall()
    # text_join_values1 = ', '.join(item[0] for item in text_join1)
    # await bot.send_message(join_request.user_chat_id, f"{text_join_values1}")

    result_join = cursor.execute('''SELECT text_join_button FROM text_command where id=1;''').fetchone()[0]

    if result_join is not None:
        text_join1 = cursor.execute("SELECT text_join FROM text_command where id=1;").fetchone()[0]
        # text_join_values1 = ', '.join(item[0] for item in text_join1)
        await bot.send_message(join_request.user_chat_id, f"{text_join1}", reply_markup=reply.keyboard_join)
        print('if')
    else:
        text_join1 = cursor.execute("SELECT text_join FROM text_command where id=1;").fetchone()[0]
        # text_join_values1 = ', '.join(item[0] for item in text_join1)
        await bot.send_message(join_request.user_chat_id, f"{text_join1}", reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
        print('else')
