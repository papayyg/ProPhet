from aiogram.dispatcher.filters.state import State, StatesGroup


class authorization(StatesGroup):
    edu = State()
    login = State()
    password = State()
