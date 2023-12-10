from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


button_menu = KeyboardButton(text='ℹ️ Показать меню')
keyboard_menu = ReplyKeyboardBuilder().row(button_menu).as_markup(resize_keyboard=True)
