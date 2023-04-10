import asyncio
from random import choice

import aioschedule
from aiogram import Dispatcher

from data.config import log_channel
from utils.db.aiomysql import BotDB

contest_word = [['Система взломана. Нанесён урон. Запущено планирование контрмер.', 'Инициирую поиск <b>пидора дня...</b>', 'Что тут у нас?', 'Офф, не дадите поспать...', "Woop-woop! That's the sound of da pidor-police!", 'Опять искать этого пидора...', 'Осторожно! <b>Пидор дня</b> активирован!', 'Сейчас поколдуем...', 'Кто сегодня счастливчик?', 'Выезжаю на поиски <b>пидора</b>', 'Итак... кто же сегодня <b>пидор дня</b>?', 'Пора запускать ракеты на Донбасс', 'Время пришло, беги пидор, беги!', 'Я почуял настоящего <b>пидора</b>'],
              ['Ну давай, посмотрим кто тут классный...' ,'<i>Ведётся поиск в базе данных</i>', '<i>Интересно...</i>', '<i>Где-же он...</i>', '<i>(Ворчит) А могли бы на работе делом заниматься</i>', '<i>Хм...</i>', '<i>Машины выехали</i>', '<i>Сканирую...</i>', '<i>Сонно смотрит на бумаги</i>', '<i>Военный спутник запущен, коды доступа внутри...</i>', '<i>Выезжаю на место...</i>', 'Как же от него говном несёт...', 'Ты думаешь спрячешься?'],
              ['Что с нами стало...', 'Доступ получен. Аннулирование протокола.', 'Не может быть!', 'Проверяю данные...', 'Так-так, что же тут у нас...', 'Тысяча чертей!', 'Так-так, что же тут у нас...', 'Ого-го...', 'Ведётся захват подозреваемого...', 'Высокий приоритет мобильному юниту.', 'В этом совершенно нет смысла...', 'Ох...', 'В рот мне слона...', 'Не верю своим глазам...', 'Вселенная что-то знает...'],
              ['Ого, вы посмотрите только! А <b>пидор дня</b> то - ', 'Что? Где? Когда? А ты <b>пидор дня</b> - ', 'Анализ завершен. Ты <b>пидор</b>, ', 'Няшный <b>пидор дня</b> - ', 'Кто бы мог подумать, но <b>пидор дня</b> - ', 'Кажется, <b>пидор дня</b> - ', '<b>Пидор дня</b> обыкновенный, 1шт. - ', 'И прекрасный человек дня сегодня... а нет, ошибка, всего-лишь <b>пидор</b> - ', 'Ну ты и <b>пидор</b>, ', 'Ага! Поздравляю! Сегодня ты <b>пидор</b> - ', '''.∧＿∧ 
( ･ω･｡)つ━☆・*。 
⊂  ノ    ・゜+. 
しーＪ   °。+ *´¨) 
         .· ´¸.·*´¨) 
          (¸.·´ (¸.·'* ☆ ВЖУХ И ТЫ ПИДОР, ''', 'Детектор не нужен, <b>пидор</b> обнаружен - ']]


async def contest_schedule(dp: Dispatcher):
    chats = await BotDB.pick_pidor()
    output = 'Победители конкурса:\n'
    for chat in chats:
        user = choice(await BotDB.users_pidor(chat[0]))
        await BotDB.user_rep(chat[0], user[1], user[0])
        pidor = f'<a href="tg://user?id={user[1]}">{user[0]}</a>'
        output += f'{pidor} в чате {chat[0]}\n'
        messages = [choice(contest_word[0]), choice(contest_word[1]), choice(contest_word[2]), f'{choice(contest_word[3])}{pidor}']
        for message in messages:
            try:
                await dp.bot.send_message(chat[0], message)
            except:
                continue
            await asyncio.sleep(3)
    await dp.bot.send_message(log_channel, f'🎉 {output}')

async def scheduler(dp):
    aioschedule.every().day.at("22:00").do(lambda: asyncio.create_task(contest_schedule(dp)))
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)

async def on_startup_contest(dp):
    asyncio.create_task(scheduler(dp))