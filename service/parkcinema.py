import aiohttp
from bs4 import BeautifulSoup

from locales.translations import _
from utils.locales import locales_dict

async def parse_parkcinema(chat_lang):
    output_film = []
    async with aiohttp.ClientSession() as session:
        url = f"https://parkcinema.az/?lang={chat_lang}"
        async with session.get(url) as response:
            soup = BeautifulSoup(await response.text(encoding='latin-1'), "html.parser")

            for item in soup.select("#frontpage-movies > div[rel=today] > .normal > .m-item"):
                details = item.find('div', class_='m-i-details')
                title = details.find('a', class_='m-i-d-title').text
                bytes_title = bytes(title, 'latin-1')
                title = bytes_title.decode('utf-8')
                temp  = f"https://parkcinema.az{details.find('a', class_='m-i-d-title').get('href')}?lang={chat_lang}"
                if not temp.startswith('https://parkcinema.az/movies/'):
                    continue
                link = f"https://mobile.parkcinema.az{details.find('a', class_='m-i-d-title').get('href')}?lang={chat_lang}"
                date  = details.find('div', class_='m-i-d-date').text
                bytes_date = bytes(date, 'latin-1')
                date = bytes_date.decode('utf-8')
                type  = details.find('div', class_='m-i-d-type').text
                lang  = ' '.join([span.text for span in details.find('div', class_='m-i-d-lang').find_all('span')])
                age  = details.find('div', class_='m-i-d-age').text
                media  = bytes(item.find('div', class_='m-i-left').find('img').get("src"), 'latin-1') .decode('utf-8')

                async with session.get(temp) as response:
                    soup = BeautifulSoup(await response.text(), 'html.parser')

                    country = soup.find("label", string=await _("Страна:", chat_lang)).find_next_sibling().text.strip()
                    year = soup.find("label", string=await _("Год", chat_lang)).find_next_sibling().text.strip()
                    director = soup.find("label", string=await _("Режиссер", chat_lang)).find_next_sibling().text.strip()
                    genre = soup.find("label", string=await _("Жанр", chat_lang)).find_next_sibling().text.strip()
                    cast = soup.find("label", string=await _("В ролях", chat_lang)).find_next_sibling().text.strip().replace("\n", ", ")
                    duration = soup.find("label", string=await _("Длительность", chat_lang)).find_next_sibling().text.strip()

                    temp = ''
                    if 'RU' in lang:
                        temp += '🇷🇺 '
                    if 'EN' in lang:
                        temp += '🇺🇸 '
                    if 'TR' in lang:
                        temp += '🇹🇷 '
                    if 'AZ' in lang:
                        temp += '🇦🇿 '
                    text = await _('<i><b>{title} ({year})</b></i>\n<b>В кинотеатре:</b> <i>{date}</i>\n<b>Страна:</b> <i>{country}</i>\n<b>Форматы:</b> {temp}<i>{type}</i>\n🧩 <b>Жанр:</b> <i>{genre}</i>\n\U0001F3A5 <b>Режиссер:</b> <i>{director}</i>\n\U0001F64D <b>В ролях:</b> <i>{cast}</i>\n\U0001F39E <b>Длительность:</b> <i>{duration}</i>\n\U0001F51E <b>Возрастные ограничения:</b> <i>{age}</i>', chat_lang)
                    
                    output_film.append([text.format(
                            title=title, year=year, date=date, country=country, temp=temp, type=type,
                            genre=genre, director=director, cast=cast, duration=duration, age=age
                        ), media, link])
    return output_film