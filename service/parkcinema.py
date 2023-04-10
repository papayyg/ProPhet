import aiohttp
from bs4 import BeautifulSoup


async def parse_parkcinema():
    output_film = []
    async with aiohttp.ClientSession() as session:
        url = "https://parkcinema.az/?lang=ru"
        async with session.get(url) as response:
            soup = BeautifulSoup(await response.text(encoding='latin-1'), "html.parser")

            for item in soup.select("#frontpage-movies > div[rel=today] > .normal > .m-item"):
                details = item.find('div', class_='m-i-details')
                title = details.find('a', class_='m-i-d-title').text
                bytes_title = bytes(title, 'latin-1')
                title = bytes_title.decode('utf-8')
                temp  = f"https://parkcinema.az{details.find('a', class_='m-i-d-title').get('href')}?lang=ru"
                if not temp.startswith('https://parkcinema.az/movies/'):
                    continue
                link = f"https://mobile.parkcinema.az{details.find('a', class_='m-i-d-title').get('href')}?lang=ru"
                date  = details.find('div', class_='m-i-d-date').text
                bytes_date = bytes(date, 'latin-1')
                date = bytes_date.decode('utf-8')
                type  = details.find('div', class_='m-i-d-type').text
                lang  = ' '.join([span.text for span in details.find('div', class_='m-i-d-lang').find_all('span')])
                age  = details.find('div', class_='m-i-d-age').text
                media  = bytes(item.find('div', class_='m-i-left').find('img').get("src"), 'latin-1') .decode('utf-8')

                async with session.get(temp) as response:
                    soup = BeautifulSoup(await response.text(), 'html.parser')

                    country = soup.find("label", string="Страна:").find_next_sibling().text.strip()
                    year = soup.find("label", string="Год").find_next_sibling().text.strip()
                    director = soup.find("label", string="Режиссер").find_next_sibling().text.strip()
                    genre = soup.find("label", string="Жанр").find_next_sibling().text.strip()
                    cast = soup.find("label", string="В ролях").find_next_sibling().text.strip().replace("\n", ", ")
                    duration = soup.find("label", string="Длительность").find_next_sibling().text.strip()

                    temp = ''
                    if 'RU' in lang:
                        temp += '🇷🇺 '
                    if 'EN' in lang:
                        temp += '🇺🇸 '
                    if 'TR' in lang:
                        temp += '🇹🇷 '
                    if 'AZ' in lang:
                        temp += '🇦🇿 '

                    output_film.append([f'<i><b>{title} ({year})</b></i>\n'
                    f'<b>В кинотеатре:</b> <i>{date}</i>\n'
                    f'<b>Страна:</b> <i>{country}</i>\n'
                    f'<b>Форматы:</b> {temp}<i>{type}</i>\n'
                    f'🧩 <b>Жанр:</b> <i>{genre}</i>\n'
                    f'\U0001F3A5 <b>Режиссер:</b> <i>{director}</i>\n'
                    f'\U0001F64D <b>В ролях:</b> <i>{cast}</i>\n'
                    f'\U0001F39E <b>Длительность:</b> <i>{duration}</i>\n'
                    f'\U0001F51E <b>Возрастные ограничения:</b> <i>{age}</i>', media, link])
    return output_film