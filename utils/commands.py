from aiogram.types import (BotCommand, BotCommandScopeAllChatAdministrators,
                           BotCommandScopeAllGroupChats, BotCommandScopeChat,
                           BotCommandScopeDefault)

from data.config import owner_id


async def set_default_commands(dp):
    commands_private = [
        BotCommand(
            command='start',
            description='Начало работы'
        ),
        BotCommand(
            command='help',
            description='Узнать подробности возможностей бота'
        ),
        BotCommand(
            command='auth',
            description=' Сохранить данные в базе (Unibook)'
        ),
        BotCommand(
            command='del',
            description='Удалить данные из базы (Unibook)'
        ),
        BotCommand(
            command='nb',
            description='Посмотреть все свои НБ (Unibook)'
        ),
        BotCommand(
            command='journal',
            description='Баллы по всем предметам (Unibook)'
        ),
        BotCommand(
            command='subjects',
            description='Информация о всех предметах (Unibook)'
        ),
        BotCommand(
            command='gpa',
            description='Средний балл за все семестры  (Unibook)'
        ),
        BotCommand(
            command='gpas',
            description='Подробный средний балл (Unibook)'
        ),
        BotCommand(
            command='cinemaplus',
            description='Кинопремьеры в CinemaPlus'
        ),
        BotCommand(
            command='parkcinema',
            description='Кинопремьеры в ParkCinema'
        ),
        BotCommand(
            command='weather',
            description='Погода в указанном городе'
        ),
        BotCommand(
            command='qbs',
            description='Добавить фото/стикер/сообщение в набор чата'
        ),
        BotCommand(
            command='dbs',
            description='Удалить стикер из набора'
        ),
        BotCommand(
            command='n',
            description='Да или нет'
        ),
        BotCommand(
            command='l',
            description='Случайное число от * до *'
        ),
        BotCommand(
            command='k',
            description='Выбор случайного варианта'
        ),
        BotCommand(
            command='ts',
            description='Текст в речь'
        ),
        BotCommand(
            command='translate',
            description='Перевести текст на русский или английский'
        ),
        BotCommand(
            command='translateto',
            description='Перевод с любого на указанный'
        ),
        BotCommand(
            command='coin',
            description='Подбросить монетку'
        ),
        BotCommand(
            command='c',
            description='Калькулятор'
        ),
        BotCommand(
            command='sound',
            description='Вырезать звук из видео'
        ),
        BotCommand(
            command='real',
            description='Сгенерировать изображение используя realisticVision'
        ),
        BotCommand(
            command='dream',
            description='Сгенерировать изображение используя dreamShaper'
        ),
        BotCommand(
            command='var',
            description='Создать вариации фотографии'
        ),
        BotCommand(
            command='link',
            description='Сократить ссылку'
        ),
        BotCommand(
            command='ping',
            description='Посмотреть состояние серверов'
        ),
    ]
    commands_group = [
        BotCommand(
            command='in',
            description='Стать участником группы'
        ),
        BotCommand(
            command='out',
            description='Перестать быть участником группы'
        ),
        BotCommand(
            command='all',
            description='Отметить всех участников группы'
        ),
        BotCommand(
            command='queerstats',
            description='Посмотреть статистику ежедневного конкурса'
        ),
        # BotCommand(
        #     command='game_help',
        #     description='Игровые команды'
        # ),
        # BotCommand(
        #     command='game',
        #     description='Подробности игр'
        # ),
        # BotCommand(
        #     command='spy_theme',
        #     description='Игровые команды'
        # ),
        # BotCommand(
        #     command='game',
        #     description='Подробности игр'
        # ),
    ]
    commands_admin = [
        BotCommand(
            command='queer',
            description='Включить ежедневный конкурс'
        ),
        BotCommand(
            command='mute',
            description='Замутить пользователя'
        ),
        BotCommand(
            command='unmute',
            description='Размутить пользователя'
        ),
        BotCommand(
            command='kick',
            description='Исключить пользователя'
        ),
        BotCommand(
            command='ban',
            description='забанить пользователя'
        ),
        BotCommand(
            command='unban',
            description='Разбанить пользователя'
        ),
        BotCommand(
            command='purge',
            description='Удалить все сообщения до указанного'
        ),
    ]
    owner_commands = [
        BotCommand(
            command='news',
            description='Отправить рассылку'
        ),
        BotCommand(
            command='runqueer',
            description='Начать конкурс'
        ),
        BotCommand(
            command='temp_look',
            description='Посмотреть содержимое temp'
        ),
        BotCommand(
            command='temp_del',
            description='Удалить содержимое temp'
        ),
        BotCommand(
            command='server_dream',
            description='Указать сервер для Dream'
        ),
        BotCommand(
            command='server_real',
            description='Указать сервер для Real'
        ),
        BotCommand(
            command='stats',
            description='Просмтр статистики'
        ),
    ]

    await dp.bot.set_my_commands(commands_private, BotCommandScopeDefault())
    await dp.bot.set_my_commands(commands_private + commands_group, BotCommandScopeAllGroupChats())
    await dp.bot.set_my_commands(commands_private + commands_group + commands_admin, BotCommandScopeAllChatAdministrators())
    await dp.bot.set_my_commands(commands_private + commands_group + commands_admin + owner_commands,BotCommandScopeChat(chat_id=owner_id))