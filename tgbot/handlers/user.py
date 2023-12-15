from aiogram import Router, Bot, F
from aiogram.filters import CommandStart, Command, or_f
from aiogram.types import Message, FSInputFile, ChatJoinRequest, ReplyKeyboardRemove, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from tgbot.keyboards.inline import keyboard
from tgbot.keyboards import reply
import time
import sqlite3
import os
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

con = sqlite3.connect('db_SQLite.db')
cursor = con.cursor()

user_router = Router()

@user_router.message(CommandStart())
async def user_start(message: Message, bot: Bot):
    print(message.from_user.id)
    text_start = cursor.execute('''SELECT text_start FROM text_command where id=1;''').fetchone()[0]
    await message.answer(f'{text_start}')


@user_router.chat_join_request()
async def chat_join_request(join_request: ChatJoinRequest, bot: Bot):
    text_start1 = cursor.execute('''SELECT text_join_button FROM text_command where id=1;''').fetchone()[0]
    button_yes = KeyboardButton(text=f'{text_start1}')
    keyboard_join = ReplyKeyboardBuilder().row(button_yes).as_markup(resize_keyboard=True)

    if cursor.execute('''SELECT text_join_button FROM text_command where id=1;''').fetchone()[0] is not None:
        text_join1 = cursor.execute('''SELECT text_join FROM text_command where id=1;''').fetchone()[0]
        await bot.send_message(join_request.user_chat_id, f'{text_join1}', reply_markup=keyboard_join)
    else:
        text_join1 = cursor.execute('''SELECT text_join FROM text_command where id=1;''').fetchone()[0]
        await bot.send_message(join_request.user_chat_id, f'{text_join1}', reply_markup=ReplyKeyboardRemove(remove_keyboard=True))

@user_router.message(F.text)
async def captcha(message: Message):

    target = cursor.execute('''SELECT text_join_button FROM text_command where id=1;''').fetchone()[0]
    if target == message.text:
        await message.answer('✅Капча пройдена!')
    else:
        pass




