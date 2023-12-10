from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, KeyboardButton, ReplyKeyboardRemove
from tgbot.keyboards.inline import keyboard, keyboard_2
from tgbot.filters.admin import AdminFilter
from tgbot.misc import SetStartMessage
from tgbot.keyboards import reply
from aiogram.methods import EditMessageReplyMarkup

import sqlite3

con = sqlite3.connect("db_SQLite.db")
cursor = con.cursor()

admin_router = Router()
admin_router.message.filter(AdminFilter())



@admin_router.message(CommandStart())
async def admin_start(message: Message, state: FSMContext):
    await state.clear()
    await message.reply("Привет, админ!", reply_markup=reply.keyboard_menu)
    await message.answer('Меню админа:', reply_markup=keyboard)
    #await message.answer('111')

@admin_router.callback_query(F.data == 'start_rename')
async def any_callback(callback: CallbackQuery, state: FSMContext):
    # await callback.message.edit_reply_markup(reply_markup=None)
    # await callback.message.edit_reply_markup()
    await state.set_state(SetStartMessage.set_message)
    await callback.message.answer(text='Введите новое сообщение для\n/start\n'
                                       'И отправьте в чат!', reply_markup=ReplyKeyboardRemove(remove_keyboard=True))



@admin_router.message(SetStartMessage.set_message)
async def set_start_message(message: Message, state: FSMContext):
     # тут берешь текст из сообщения и засовываешь в БД
     answer = message.text
     cursor.execute('''UPDATE text_command SET text_start = ?;''', (answer,))
     con.commit()
     await state.clear() # очищаешь состояние
     # await message.answer(f'Вы написали {answer}')
     result = cursor.execute('''SELECT text_start FROM text_command;''').fetchone()

     if result is not None and result[0] is not None:
         await message.answer("✅ Новое приветственное сообщение сохранено!")
     else:
         await message.answer("❌ Ошибка сохранения! ❌\n"
                              "Вы можете добавлять только\n"
                              "текст, ссылки, эмодзи 🥹")

     con.commit()

@admin_router.callback_query(F.data == 'join_rename' )
async def any_callback_join(callback: CallbackQuery, state: FSMContext):
    #await callback.message.edit_text('Тестовый текст')
    await state.set_state(SetStartMessage.set_message_join)
    await callback.message.answer(text='Введите новое сообщение приветствие, подписки на Канал. И отправьте в чат!\n')

@admin_router.message(SetStartMessage.set_message_join)
async def set_start_message_join(message: Message, state: FSMContext):
     # тут берешь текст из сообщения и засовываешь в БД
     answer_join = message.text
     cursor.execute('''UPDATE text_command SET text_join = ?;''', (answer_join,))
     con.commit()
     await state.clear() # очищаешь состояние
     # await message.answer(f'Вы написали {answer}')
     result_join = cursor.execute('''SELECT text_join FROM text_command;''').fetchone()

     if result_join is not None and result_join[0] is not None:
         await message.answer("✅ Новое приветственное сообщение для Канала сохранено!")
     else:
         await message.answer("❌ Ошибка сохранения! ❌\n"
                              "Вы можете добавлять только\n"
                              "текст, ссылки, эмодзи 🥹")

     con.commit()

@admin_router.message(F.text == 'ℹ️ Показать меню')
async  def set_menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Меню админа:', reply_markup=keyboard)

@admin_router.callback_query(F.data == 'sender_users')
async  def sending(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer('✉️ Рассылка', reply_markup=keyboard_2)
    await callback.message.delete_reply_markup()
    await callback.message.delete()
