import aiohttp


async def baku():
    async with aiohttp.ClientSession() as session:
        async with session.get('http://ip-api.com/json/') as response:
            location_data = await response.json()
            if location_data["countryCode"] == 'AZ':
                return 1
            else:
                return 0
