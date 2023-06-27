import re

from aiogram import types

from loader import dp
from service.converter import currency_converter

from utils.logs import send_logs


@dp.message_handler(lambda message: re.match(r'^\d+\s+\w{3}\s+to\s+\w{3}$', message.text) or re.match(r'^\d+\.\d+\s+\w{3}\s+to\s+\w{3}$', message.text))
async def handler(message: types.Message):
    if re.match(r'^\d+\.\d+', message.text):
        amount = float(re.match(r'^\d+\.\d+', message.text).group())
    else: amount = int(re.match(r'^\d+', message.text).group())
    from_currency = re.search(r'\b\w{3}\b', message.text.split(' to ')[0].strip().split()[-1]).group().upper()
    to_currency = re.search(r'\b\w{3}\b\s+to\s+\b(\w{3})\b', message.text).group(1).upper()
    try:
        result = await currency_converter(amount, from_currency, to_currency)
        if len(str(result).split(".")[0]) >= 5:
            result = '{:,}'.format(int(str(result).split(".")[0])).replace(',', ' ')
        await message.answer(f'{result} {to_currency}')
    except Exception as ex:
        await message.answer(f'⚠️ Error: {ex}')
    await send_logs(message.from_user.first_name, message.text)