from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
# from aiogram.utils.keyboard import InlineKeyboardBuilder

# -------------------------------------------------------------------------------------------------------- keyboard back
url_button_1 = InlineKeyboardButton(
    text='🗯 Изменить текст /start',
    callback_data='start_rename'
)
url_button_2 = InlineKeyboardButton(
    text='✍️ Изменить текст подписки на Канал',
    callback_data='join_rename'
)
url_button_3 = InlineKeyboardButton(
    text='✉️ Рассылка',
    callback_data='sender_users'
)

# Создаем объект инлайн-клавиатуры
keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[[url_button_1],
                     [url_button_2],
                     [url_button_3]]
)



sms_sending = InlineKeyboardButton(
    text='Задать текст для смс',
    callback_data='cd_sms_sending'
)
start_sms_sending = InlineKeyboardButton(
    text='Начать рассылку',
    callback_data='cd_sms_sending'
)
keyboard_2: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[[sms_sending],
                     [start_sms_sending]]
)

yes_button = InlineKeyboardButton(text='Да✅', callback_data='yes')
no_button = InlineKeyboardButton(text='Нет❌', callback_data='no')
keyboard_3: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[[yes_button,no_button]]
)

rename_button_yes = InlineKeyboardButton(text='Задать текст кнопки', callback_data='rename_button_yes')

# --------------------------------------------------------------------------------------------------- keyboard yes or no
