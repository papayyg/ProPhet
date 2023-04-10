from aiogram.dispatcher.filters.state import State, StatesGroup


class authorization(StatesGroup):
    login = State()
    password = State()
