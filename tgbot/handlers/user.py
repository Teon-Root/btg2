from aiogram import Router, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile, ChatJoinRequest
from tgbot.keyboards.inline import keyboard
import time
import sqlite3
import os

con = sqlite3.connect("db_SQLite.db")
cursor = con.cursor()
text_start = cursor.execute("SELECT text_start FROM main.text_command;").fetchall()
text_start_values = ', '.join(item[0] for item in text_start)
print(text_start_values)

text_join = cursor.execute("SELECT text_join FROM main.text_command;").fetchall()
text_join_values = ', '.join(item[0] for item in text_join)
print(text_join_values)



user_router = Router()


@user_router.message(CommandStart())
async def user_start(message: Message, bot: Bot):
    await message.answer(f"{text_start_values}")

@user_router.chat_join_request()
async def chat_join_request(join_request: ChatJoinRequest, bot: Bot):
    await bot.send_message(join_request.user_chat_id, f"{text_join_values}")

