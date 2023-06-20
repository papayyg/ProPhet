import logging

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import filters
from data import config

logging.basicConfig(handlers=[logging.FileHandler('logs.log', 'a', 'utf-8'),
                                logging.StreamHandler()], 
                                level=logging.INFO, 
                                format="%(asctime)s %(message)s")
bot = Bot(token=config.API_TOKEN, parse_mode=types.ParseMode.HTML)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
filters.setup(dp) 