from aiogram import Dispatcher

from .throttling import ThrottlingMiddleware

# from .logging import LoggingMiddleware


def setup(dp: Dispatcher):
    dp.middleware.setup(ThrottlingMiddleware())
    # dp.middleware.setup(LoggingMiddleware())