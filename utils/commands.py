from aiogram.types import (BotCommand, BotCommandScopeAllChatAdministrators,
                           BotCommandScopeAllGroupChats, BotCommandScopeChat,
                           BotCommandScopeDefault)

from data.config import owner_id

from locales.translations import _
from utils.locales import locales_dict

async def commands_private(lang):
    commands_p = [
        BotCommand(
            command='start',
            description=await _('Начало работы', lang)
        ),
        BotCommand(
            command='help',
            description=await _('Узнать подробности возможностей бота', lang)
        ),
        BotCommand(
            command='auth',
            description=await  _('Сохранить данные в базе (Unibook, Empro)', lang)
        ),
        BotCommand(
            command='del',
            description=await _('Удалить данные из базы (Unibook, Empro)', lang)
        ),
        BotCommand(
            command='nb',
            description=await _('Посмотреть все свои НБ (Unibook, Empro)', lang)
        ),
        BotCommand(
            command='journal',
            description=await _('Баллы по всем предметам (Unibook, Empro)', lang)
        ),
        BotCommand(
            command='subjects',
            description=await _('Информация о всех предметах (Unibook)', lang)
        ),
        BotCommand(
            command='gpa',
            description=await _('Средний балл за все семестры  (Unibook)', lang)
        ),
        BotCommand(
            command='gpas',
            description=await _('Подробный средний балл (Unibook)', lang)
        ),
        BotCommand(
            command='cinemaplus',
            description=await _('Кинопремьеры в CinemaPlus', lang)
        ),
        BotCommand(
            command='parkcinema',
            description=await _('Кинопремьеры в ParkCinema', lang)
        ),
        BotCommand(
            command='weather',
            description=await _('Погода в указанном городе', lang)
        ),
        BotCommand(
            command='qbs',
            description=await _('Добавить фото/стикер/сообщение в набор чата', lang)
        ),
        BotCommand(
            command='dbs',
            description=await _('Удалить стикер из набора', lang)
        ),
        BotCommand(
            command='n',
            description=await _('Да или нет', lang)
        ),
        BotCommand(
            command='l',
            description=await _('Случайное число от * до *', lang)
        ),
        BotCommand(
            command='k',
            description=await _('Выбор случайного варианта', lang)
        ),
        BotCommand(
            command='ts',
            description=await _('Текст в речь', lang)
        ),
        BotCommand(
            command='translate',
            description=await _('Перевести текст на русский или английский', lang)
        ),
        BotCommand(
            command='translateto',
            description=await _('Перевод с любого на указанный', lang)
        ),
        BotCommand(
            command='coin',
            description=await _('Подбросить монетку', lang)
        ),
        BotCommand(
            command='c',
            description=await _('Калькулятор', lang)
        ),
        BotCommand(
            command='sound',
            description=await _('Вырезать звук из видео', lang)
        ),
        BotCommand(
            command='real',
            description=await _('Сгенерировать изображение используя realisticVision', lang)
        ),
        BotCommand(
            command='dream',
            description=await _('Сгенерировать изображение используя dreamShaper', lang)
        ),
        BotCommand(
            command='var',
            description=await _('Создать вариации фотографии', lang)
        ),
        BotCommand(
            command='link',
            description=await _('Сократить ссылку', lang)
        ),
        BotCommand(
            command='ping',
            description=await _('Посмотреть состояние серверов', lang)
        ),
        BotCommand(
            command='lang',
            description=await _('Сменить язык', lang)
        ),
    ]
    return commands_p

async def commands_group(lang):
    commands_group = [
        BotCommand(
            command='in',
            description=await _('Стать участником группы', lang)
        ),
        BotCommand(
            command='out',
            description=await _('Перестать быть участником группы', lang)
        ),
        BotCommand(
            command='all',
            description=await _('Отметить всех участников группы', lang)
        ),
        BotCommand(
            command='queerstats',
            description=await _('Посмотреть статистику ежедневного конкурса', lang)
        ),
    ]
    return commands_group


async def commands_admin(lang):
    commands_admin = [
        BotCommand(
            command='queer',
            description=await _('Включить ежедневный конкурс', lang)
        ),
        BotCommand(
            command='mute',
            description=await _('Замутить пользователя', lang)
        ),
        BotCommand(
            command='unmute',
            description=await _('Размутить пользователя', lang)
        ),
        BotCommand(
            command='kick',
            description=await _('Исключить пользователя', lang)
        ),
        BotCommand(
            command='ban',
            description=await _('Забанить пользователя', lang)
        ),
        BotCommand(
            command='unban',
            description=await _('Разбанить пользователя', lang)
        ),
        BotCommand(
            command='purge',
            description=await _('Удалить все сообщения до указанного', lang)
        ),
    ]
    return commands_admin

async def owner_commands(lang):
    owner_commands = [
        BotCommand(
            command='news',
            description=await _('Отправить рассылку', lang)
        ),
        BotCommand(
            command='runqueer',
            description=await _('Начать конкурс', lang)
        ),
        BotCommand(
            command='temp_look',
            description=await _('Посмотреть содержимое temp', lang)
        ),
        BotCommand(
            command='temp_del',
            description=await _('Удалить содержимое temp', lang)
        ),
        BotCommand(
            command='server_dream',
            description=await _('Указать сервер для Dream', lang)
        ),
        BotCommand(
            command='server_real',
            description=await _('Указать сервер для Real', lang)
        ),
        BotCommand(
            command='stats',
            description=await _('Просмотр статистики', lang)
        ),
    ]
    return owner_commands

async def set_default_commands(dp):
    for chat_id, lang in locales_dict.items():
        if chat_id > 0:
            try:
                await dp.bot.set_my_commands(await commands_private(lang), BotCommandScopeChat(chat_id=chat_id))
            except:
                continue
        else:
            try:
                await dp.bot.set_my_commands(await commands_private(lang) + await commands_group(lang), BotCommandScopeAllGroupChats())
                await dp.bot.set_my_commands(await commands_private(lang) + await commands_group(lang) + await commands_admin(lang), BotCommandScopeAllChatAdministrators())
            except:
                continue
    await dp.bot.set_my_commands(await commands_private('ru') + await commands_group('ru') + await commands_admin('ru') + await owner_commands('ru'), BotCommandScopeChat(chat_id=owner_id))

async def set_command_lang(dp, chat_id, lang):
    await dp.bot.set_my_commands(await commands_private(lang), BotCommandScopeChat(chat_id=chat_id))