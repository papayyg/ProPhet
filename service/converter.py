import aiohttp

from data.config import CURRENCY_API


async def currency_converter(amount, from_currency, to_currency):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://v6.exchangerate-api.com/v6/{CURRENCY_API}/latest/{from_currency}") as response:
            data = await response.json()
            rate = data['conversion_rates'][to_currency]
            result = amount * rate
            if len(str(result)[str(result).find('.'):]) > 4:
                result = format(result, '.4f')
            return result
