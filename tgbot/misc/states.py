from aiogram.fsm.state import StatesGroup, State


class SetStartMessage(StatesGroup):
    set_message = State()
    set_message_join = State()