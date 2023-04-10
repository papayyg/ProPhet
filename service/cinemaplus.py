import aiohttp
from bs4 import BeautifulSoup


async def parse_cinemaplus():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://cinemaplus.az/ru/") as response:
            html = BeautifulSoup(await response.text(), 'html.parser')
            films = {}
            for el in html.select(".movies > .row > .sortable_movie_home"):
                select = el.select('h2 > a')
                photo = f"http://cinemaplus.az{el.select('.movie_image > a > div > img')[0].get('src')}"
                link = select[0].get("href")
                title = select[0].text
                async with session.get(f"https://cinemaplus.az{link}") as response:
                    link = f"https://cinemaplus.az{link}"
                    soup = BeautifulSoup(await response.text(), 'html.parser')
                    meta = {}
                    for ro in soup.select(".tabs > .tab_body > .tab > .right_banner > .movie_details > .md_new > .movie_details1 > li"):
                        info = ro.select('span')[0].text
                        data = ro.select('div')[0].text
                        meta[info] = data
                    films[title] = meta, photo, link
            premier = []
            for i in films:
                str = ''
                form = films[i][0]["Форматы"]
                if 'Стендап' in form:
                    str += 'Стендап '
                if 'азербайджанском' in form:
                    str += '\U0001F1E6\U0001F1FF '
                if '4DX' in form:
                    str += '4DX '
                if '3D' in form:
                    str += '3D '
                if '2D' in form:
                    str += '2D '
                if 'русском' in form:
                    str += '\U0001F1F7\U0001F1FA '
                if 'английском' in form:
                    str += '\U0001F1EC\U0001F1E7 '
                if 'турецком' in form:
                    str += '\U0001F1F9\U0001F1F7 '
                if 'азербайджанскими' in form:
                    str += '\U0001F1E6\U0001F1FFSUB '
                premier.append([f'<i><b>{i}</b></i>\n'
                f'<b>В кинотеатре:</b> <i>{films[i][0]["В кинотеатре"]}</i>\n'
                f'<b>Страна:</b> <i>{films[i][0]["Страна"]}</i>\n'
                f'<b>Форматы:</b> <i>{str}</i>\n'
                f'🧩 <b>Жанр:</b> <i>{films[i][0]["Жанр"]}</i>\n'
                f'\U0001F3A5 <b>Режиссер:</b> <i>{films[i][0]["Режиссер"]}</i>\n'
                f'\U0001F64D <b>В ролях:</b> <i>{films[i][0]["В ролях"]}</i>\n'
                f'\U0001F39E <b>Длительность:</b> <i>{films[i][0]["Длительность"]}</i>\n'
                f'\U0001F51E <b>Возрастные ограничения:</b> <i>{films[i][0]["Возрастные ограничения"]}</i>', films[i][1], films[i][2]])
    return premier