from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
# from aiogram.utils.keyboard import InlineKeyboardBuilder

# -------------------------------------------------------------------------------------------------------- keyboard back
url_button_1 = InlineKeyboardButton(
    text='Изменить текст /start',
    callback_data='start_rename'
)
url_button_2 = InlineKeyboardButton(
    text='Изменить текст join',
    callback_data='join_rename'
)
url_button_3 = InlineKeyboardButton(
    text='Рассылка',
    callback_data='sender_users'
)


# Создаем объект инлайн-клавиатуры
keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[[url_button_1],
                     [url_button_2],
                     [url_button_3]]
)


# --------------------------------------------------------------------------------------------------- keyboard yes or no
