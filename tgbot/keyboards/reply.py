from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
import sqlite3

con = sqlite3.connect("db_SQLite.db")
cursor = con.cursor()

button_menu = KeyboardButton(text='ℹ️ Показать меню')
keyboard_menu = ReplyKeyboardBuilder().row(button_menu).as_markup(resize_keyboard=True)

text_start1 = cursor.execute("SELECT text_join_button FROM text_command where id=1;").fetchone()[0]

button_yes = KeyboardButton(text=f'{text_start1}')

keyboard_join = ReplyKeyboardBuilder().row(button_yes).as_markup(resize_keyboard=True)
print('Вот', text_start1)