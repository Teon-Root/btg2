from aiogram import Router, Bot, F
from aiogram.filters import CommandStart, Command, or_f
from aiogram.types import Message, FSInputFile, ChatJoinRequest, ReplyKeyboardRemove, KeyboardButton, ChatMemberUpdated
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from tgbot.keyboards.inline import keyboard
from tgbot.keyboards import reply
import time
import sqlite3
import os
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters.chat_member_updated import ChatMemberUpdatedFilter, MEMBER, KICKED

con = sqlite3.connect('db_SQLite.db')
cursor = con.cursor()

user_router = Router()

@user_router.message(CommandStart())
async def user_start(message: Message, bot: Bot):
    text_start = cursor.execute('''SELECT text_start FROM text_command where id=1;''').fetchone()[0]
    await message.answer(f'{text_start}')
    user_id = message.from_user.id
    print(user_id)
    # existing_user = cursor.execute(f'''SELECT user_id FROM user_table WHERE user_id = 5603001487;''').fetchone()[0]
    # print('запрос',existing_user)
    try:
        existing_user = await cursor.execute(f'''SELECT user_id FROM user_table WHERE user_id = 5603001487;''').fetchone()[0]
        print('запрос', existing_user)
        if not existing_user:
            cursor.execute('''INSERT INTO user_table (user_id) VALUES (?);''', (user_id,))
            con.commit()
            print('мы записали в базу', user_id)
    except TypeError:
        cursor.execute('''INSERT INTO user_table (user_id) VALUES (?);''', (user_id,))
        con.commit()
        print('мы записали в базу', user_id)
    pass

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
    target = cursor.execute('''SELECT text_join_button FROM text_command WHERE id = 1;''').fetchone()[0]

    if target == message.text:
        await message.answer('✅Капча пройдена!')
        user_id = message.from_user.id
        existing_user = cursor.execute('''SELECT user_id FROM user_table WHERE user_id = ?;''', (user_id,)).fetchone()

        if not existing_user:
            cursor.execute('''INSERT INTO user_table (user_id) VALUES (?);''', (user_id,))
            con.commit()
        pass
@user_router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED))
async def user_blocked_bot(event: ChatMemberUpdated):
    kicked = int(event.from_user.id)
    print(kicked)
    cursor.execute('''DELETE FROM user_table WHERE user_id = ?;''', (kicked,))
    con.commit()
    print(f'удалили с базы {kicked}')




