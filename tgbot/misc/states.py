from aiogram.fsm.state import StatesGroup, State


class SetStartMessage(StatesGroup):
    set_message = State()
    set_message_join = State()
    set_message_yes = State()
    set_message_no = State()
    cd_sms_sending = State()
    cd_sms_start = State()