from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, KeyboardButton, ReplyKeyboardRemove
from tgbot.keyboards.inline import keyboard, keyboard_2, keyboard_3
from tgbot.filters.admin import AdminFilter
from tgbot.misc import SetStartMessage
from tgbot.keyboards import reply
from aiogram.methods import EditMessageReplyMarkup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import sqlite3

con = sqlite3.connect("db_SQLite.db")
cursor = con.cursor()

admin_router = Router()
admin_router.message.filter(AdminFilter())

@admin_router.message(CommandStart())
async def admin_start(message: Message, state: FSMContext):
    print(message.from_user.id)
    await state.clear()
    await message.reply("Привет, админ!", reply_markup=reply.keyboard_menu)
    await message.answer('Меню админа:', reply_markup=keyboard)

@admin_router.callback_query(F.data == 'start_rename')
async def any_callback(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SetStartMessage.set_message)
    await callback.message.answer(text='Введите новое сообщение для\n/start\n'
                                       'И отправьте в чат!', reply_markup=ReplyKeyboardRemove(remove_keyboard=True))

@admin_router.message(SetStartMessage.set_message)
async def set_start_message(message: Message, state: FSMContext):
     answer = message.text
     cursor.execute(f'''UPDATE text_command SET text_start = '{answer}' where id=1;''')
     con.commit()
     await state.clear()
     result = cursor.execute('''SELECT text_start FROM text_command where id=1;''').fetchone()[0]
     if result != 'None':
         await message.answer("✅ Новое приветственное сообщение сохранено!", reply_markup=reply.keyboard_menu)
         await state.clear()
     else:
         await message.answer("❌ Ошибка сохранения! ❌\n"
                              "Вы можете добавлять только\n"
                              "текст, ссылки, эмодзи 🥹", reply_markup=reply.keyboard_menu)

     con.commit()

@admin_router.callback_query(F.data == 'join_rename' )
async def any_callback_join(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SetStartMessage.set_message_join)
    await callback.message.answer(text='Введите новое сообщение приветствие, подписки на Канал. И отправьте в чат!\n', reply_markup=ReplyKeyboardRemove(remove_keyboard=True))

@admin_router.message(SetStartMessage.set_message_join)
async def set_start_message_join(message: Message, state: FSMContext):
     answer_join = message.text
     await state.clear()
     result_join = cursor.execute(f'''UPDATE text_command SET text_join ='{answer_join}' where id=1;''')
     con.commit()
     print(result_join)

     if cursor.execute('''SELECT text_join FROM text_command where id=1;''').fetchone()[0] != 'None':
         await message.answer("✅ Новое приветственное сообщение для Канала сохранено!", reply_markup=reply.keyboard_menu)
         await state.clear()
         await message.answer('Добавим Кнопку📌 в приветствие ?', reply_markup=keyboard_3)
     else:
         await message.answer("❌ Ошибка сохранения! ❌\n"
                              "Вы можете добавлять только\n"
                              "текст, ссылки, эмодзи 🥹", reply_markup=reply.keyboard_menu)


@admin_router.callback_query(F.data == 'no')
async def no_callback(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SetStartMessage.set_message_no)
    await callback.message.answer(text='Сохранено!\nБот работает✅ Без кнопки', reply_markup=reply.keyboard_menu)
    cursor.execute('''UPDATE text_command SET text_join_button = NULL WHERE id = 1;''')
    con.commit()
    await state.clear()

@admin_router.callback_query(F.data == 'yes')
async def yes_callback(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SetStartMessage.set_message_yes)
    await callback.message.answer(text='Да✅ Давай настроем кнопку:\nотправьте текст-название в чат! ', reply_markup=ReplyKeyboardRemove(remove_keyboard=True))

@admin_router.message(SetStartMessage.set_message_yes)
async def set_message_yes(message: Message, state: FSMContext):
    answer_join_button = message.text
    cursor.execute(f'''UPDATE text_command SET text_join_button = '{answer_join_button}' where id=1;''')
    con.commit()
    await state.clear()
    result_join = cursor.execute('''SELECT text_join_button FROM text_command where id=1;''').fetchone()[0]
    print(result_join)
    if result_join != 'None':
        await message.answer("✅ Текст для кнопки сохранён!\nБот работает✅", reply_markup=reply.keyboard_menu)
        await state.clear()
    else:
        await message.answer("❌ Ошибка сохранения! ❌\n"
                             "Кнопка может содержать только\n"
                             "текст, эмодзи 🥹", reply_markup=reply.keyboard_menu)
        await message.answer('Добавим Кнопку📌 в приветствие ?', reply_markup=keyboard_3)

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
    result_join = cursor.execute('''SELECT text_newsletter FROM text_command where id=1;''').fetchone()[0]
    sep = '...........................................................'
    await callback.message.answer(f'<b>Сейчас текст рассылки такой:</b>\n{sep}\n{result_join}')


@admin_router.callback_query(F.data == 'cd_sms_sending')
async def yes_callback(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SetStartMessage.cd_sms_sending)
    await callback.message.answer(text='Напиши текст для рассылки и отправь в чат! ', reply_markup=ReplyKeyboardRemove(remove_keyboard=True))

@admin_router.message(SetStartMessage.cd_sms_sending)
async def set_message_yes(message: Message, state: FSMContext):
    text_newsletter = message.text
    cursor.execute(f'''UPDATE text_command SET text_newsletter = '{text_newsletter}' where id=1;''')
    con.commit()
    await state.clear()
    result_join = cursor.execute('''SELECT text_newsletter FROM text_command where id=1;''').fetchone()[0]
    print(result_join)
    if result_join != 'None':
        await message.answer("✅ Текст для рассылки сохранён", reply_markup=reply.keyboard_menu)
        await state.clear()
    else:
        await message.answer("❌ Ошибка сохранения! ❌\n"
                             "Сообщение может содержать только\n"
                             "текст, эмодзи 🥹", reply_markup=reply.keyboard_menu)