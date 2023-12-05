from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message
from tgbot.keyboards.inline import keyboard

from tgbot.filters.admin import AdminFilter


admin_router = Router()
admin_router.message.filter(AdminFilter())


@admin_router.message(CommandStart())
async def admin_start(message: Message):
    await message.reply("Привет, админ!")
    await message.answer('Меню админа: ',reply_markup=keyboard)

@admin_router.callback_query(F.data == 'start_rename')
async def any_callback(callback: CallbackQuery):
    print('калбек')
    await callback.message.edit_text('Тестовый текст')
    await callback.message.answer(text='Тестовый текст 2')
    print('калбек')
    await callback.answer()
    print('калбек')
