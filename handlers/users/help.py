from aiogram import types

from loader import dp
from utils.db.aiomysql import BotDB
from utils.misc.throttling import rate_limit


from locales.translations import _
from utils.locales import locales_dict

help_msg = '''<i><b>Все команды бота:</b></i>
<b>Префиксы команд: / @ !</b>

/n - Бот отвечает "Да" или "Нет"
/l <i><b>*от*</b></i> <i><b>*до*</b></i> - Выбрать случайное число в промежутке
/k <i><b>*Перечисление вариантов через пробел*</b></i> - Выбор случайного варианта из указанных
/coin - Бот подбросит монетку
/c <i><b>*математическое выражение*</b></i> - Вычислить ответ для мат. выражения (/c_help для получения подробностей)
/sound - Отправьте ответом на видео, чтобы вырезать звук из него.
Шар, <i>"Вопрос"</i> - Спросить у магического шара

<i>Отправьте голосовое сообщение, чтобы преобразовать его в текст</i>
<i>Обратитесь к боту (бот,) в начале ГС, чтобы отправить запрос GPT через голос</i>
/ts <i><b>*Текст*</b></i>- Перевод текста в речь

/parkcinema - Посмотреть список премьер в кинотеатрах ParkCinema
/cinemaplus - Посмотреть список премьер в кинотеатрах CinemaPlus

/link <b>*ссылка*</b> - Вернет сокращенную ссылку
/weather <i><b>название города на англ. или русс.</b></i> - Посмотреть погоду в Баку или указанном городе
/translate - Для перевода с русского на английский или с любого другого языка на русский
/translateto <i><b>код языка</b></i> - Для перевода с любого языка на указанный (<a href="https://www.fincher.org/Utilities/CountryLanguageList.shtml">Код</a> языка указывать в виде двух букв)
<i>значение</i> <b>из валюты</b> to <b>в валюту</b> - Конвертировать валюту (Пример: 100 usd to azn)

<i>Напишите в чате [ууу, гост, хоко, уэнсдей, густас] чтобы отправить соответствующую музыку</i>

/qbs - Отправьте ответом на фото/стикер/текстовое сообщение, чтобы добавить стикер в пак чата
/dbs - Отправьте ответом на стикер из пака чата, чтобы удалить его из набора

<i>Отправьте ссылку на фото или видео <b>Instagram</b>, чтобы скачать</i>
<i>Отправьте ссылку на <b>TikTok</b>, чтобы скачать видео без водяного знака</i>
<i>Отправьте ссылку на <b>Youtube Shorts</b>, чтобы скачать видео</i>
<i>Отправьте ссылку на <b>Youtube видео</b> до 3.5 минут, чтобы скачать его</i>

Напишите бот,  или bot, и дальше после запятой интересующая вас тема или вопрос, чтоб отправить запрос боту GPT
Напишите фото,  или image, и дальше после запятой образ, который должен нарисовать ИИ
/var - Напишите ответом на фото, чтобы создать вариации его

<i>Тестовые функции, могут не всегда работать</i>
/real <b>*promt*</b> - Сгенерировать изображение используя модель Realistic Vision v2
/dream <b>*promt*</b> - Сгенерировать изображение используя модель Dream Shaper 4

/start - Приветственное сообщение
/help - Помощь по функционалу
/ping - Посмотреть состояние серверов
/lang - Сменить язык'''

help_msg_az = '''<i><b>Bütün bot əmrləri</b></i>
<b>Əmr prefiksləri: / @ !</b>

/n - Bot "Bəli" və ya "Xeyr" cavabı verir
/l <i><b>*dən*</b></i> <i><b>*qədər*</b></i> - Intervalda təsadüfi sayı seçir
/k <i><b>*Boşluqlarla ayrılmış seçimlərin siyahısı*</b></i> - Göstərilənlərdən təsadüfi seçim
/coin - Bot sikkə çevirəcək
/c <i><b>*riyaziyyat ifadəsi*</b></i> - Riyaziyyat ifadəsi üçün cavabı hesablayın (ətraflı məlumat üçün/c_help)
/sound - Videodan səsi kəsmək üçün ona cavab verin.
Kürə, <i>"Sual"</i> - Sehrli kürədən soruş

<i>Mətnə çevirmək üçün səsli mesaj göndərin</i>
<i>Səs vasitəsilə GPT sorğusu göndərmək üçün səsli mesajın əvvəlindəki botla (bot,) əlaqə saxlayın</i>
/ts <i><b>*Mətn*</b></i>- Mətndən nitqə tərcümə

/parkcinema - ParkCinema kinoteatrlarındakı premyeraların siyahısına baxın
/cinemaplus - CinemaPlus kinoteatrlarındakı premyeraların siyahısına baxın

/link <b>*link*</b> - Qısaldılmış keçidi qaytarır
/hava <i><b>İngiliscə şəhər adı və ya az</b></i> - Bakıda və ya müəyyən şəhərdə havaya baxın
/translate - Rus dilindən ingilis dilinə və ya hər hansı digər dildən rus dilinə tərcümə etmək
/translateto <i><b>dil kodu</b></i> - İstənilən dildən göstərilən dilə tərcümə etmək üçün (<a href="https://www.fincher.org/Utilities/CountryLanguageList.shtml" >Kod </a> dilləri iki hərf kimi göstərilməlidir)
<i>dəyər</i> <b>valyutadan</b> to <b>valyutaya</b> - Valyutanı çevir (Məsələn: 100 usd to azn)

/qbs - Stikeri söhbət paketinə əlavə etmək üçün foto/stiker/mətn mesajına cavab verin
/dbs - Paketdən silmək üçün söhbət paketindən stikerə cavab verin

<i>Endirmək üçün foto və ya video linkini <b>Instagram</b>-a göndərin</i>
<i>Su nişanı olmadan video yükləmək üçün <b>TikTok</b>-a keçid göndərin</i>
<i>Videonu endirmək üçün <b>Youtube Shorts</b>-a keçid göndərin</i>
<i>Endirmək üçün <b>Youtube videosuna</b> 3,5 dəqiqəyə qədər link göndərin</i>

GPT botuna sorğu göndərmək üçün bot və ya bot, ardınca vergül, maraqlandığınız mövzu və ya sualı yazın
Foto və ya şəkil yazın, sonra vergüldən sonra AI-nin çəkməli olduğu şəkli yazın.
/var - Fotonun variasiyalarını yaratmaq üçün ona cavab yazın

<i>Тестовые функции, могут не всегда работать</i>
/real <b>*promt*</b> - Сгенерировать изображение используя модель Realistic Vision v2
/dream <b>*promt*</b> - Сгенерировать изображение используя модель Dream Shaper 4

/start - Xoş gəlmisiniz mesajı
/help - Funksionallıqla bağlı yardım
/ping - Server statusuna baxın
/lang - Dil dəyışmək'''

help_unibook = '''<b>🛢 Unibook (ASOIU) и ✈️ Empro (NAA):</b>
/auth - Сохранить данные в базе, без этого не будут доступны команды
❗️<b>Пароли хранятся на защищенном сервере, никто доступа к ним не имеет. В случае недоверия, смените пароль на случайный в настройках Unibook или Empro и после пользуйтесь этой функцией!</b>
/del - Удалить сохраненные данные из базы
/nb - Посмотреть все НБ по всем предметам
/journal - Посмотреть итоговый журнал за семестр

<b>Unibook</b>
/gpa - Посчитать средний балл за все семестры (Долгий процесс)
/gpas - Посмотреть баллы и кредиты за каждый предмет всех семестров с выводом среднего балла (Долгий процесс)
/subjects - Посмотреть всю информацию о каждом предмете, а также скачать файлы предмета (Лекции, силлабус и т.п.)

Алиасы: <code>вход</code>, <code>нб</code>, <code>журнал</code>, <code>предметы</code>'''

help_unibook_az = '''<b>🛢 Unibook (ASOIU) və ✈️ Empro (NAA):</b>
/auth - Qeydiyyat məlumatları yadda saxla, əks halda əmrlər mövcud olmayacaq
❗️<b>Parollar təhlükəsiz serverdə saxlanılır.  Etibarsızlıq halında, Unibook və ya Empro parametrlərində parolu dəyişin və sonra bu funksiyadan istifadə edin!</b>
/del - Yadda saxlanan məlumatları silir
/nb - Fənlər üzrə qayıblərə baxın
/journal - Semestr üçün yekun jurnala baxın

<b>Unibook</b>
/gpa - Bütün semestrlər üçün ÜOMG hesablayın (Uzun proses)
/gpas - ÜOMG nəticəsi ilə bütün semestrlərin hər bir fənni üzrə qiymətlərə və kreditlərə baxın (Uzun proses)
/subjects - Fənnlər haqqında bütün məlumatlara baxın və elektron materialları yükləyin (mühazirələr, sillabus və s.)'''

help_group = '''<b>Команды для группы</b>
<b><i>❗️Для работы некоторые функций (По типу GPT), нужно выдать права администратора боту</i></b>

/in - Стать участником группы
/out - Перестать быть участником группы
/queer - Включить ежедневный конкурс (Только для администратора)
/queerstats - Посмотреть статистику ежедневного конкурса группы
/all - Отметить всех участников группы
<b>*Все следующие команды работают ответом на сообщение:</b>
/mute <i>*число* *причина*</i> - Замутит пользователя на указанное время в минутах, можно и не указывать (/mute 10 мат)
/unmute - Снять мут с пользователя
/kick - Исключить из группы
/ban - Заблокировать пользователя в группе
/unban - Разблокировать пользователя
/purge - Удалить все сообщения до указанного'''

help_group_az = '''<b>Qrup Əmrləri</b>

 /in - Qrup üzvü olmaq
 /out - Qrupu tərk etmək
 /queer - Gündəlik müsabiqəni aktivləşdirmək (yalnız admin)
 /queerstats - Qrupun gündəlik müsabiqə statistikasına baxın
 /all - Bütün qrup üzvlərini işarələmək
 <b>*Aşağıdakı əmrlərin hamısı mesaja cavab kimi işləyir:</b>
 /mute <i>*nömrə* *səbəb*</i> - İstifadəçini dəqiqələrlə müəyyən edilmiş müddət ərzində səssizləşdirir, bunu qeyd etməməkdə olar (/mute 10 söyüş)
 /unmute - İstifadəçinin səsini açır
 /kick - Qrupdan çıxartmaq
 /ban - Ban etmək
 /unban - Bannan çıxartmaq
 /purge - Verilmiş mesaja qədər çatı silmək'''


@rate_limit(limit=5)
@dp.message_handler(commands=['help_all'], commands_prefix="/!@")
async def command_help_all(message: types.Message):
    if locales_dict[message.chat.id] == 'ru':
        await message.answer(help_msg, disable_web_page_preview=True)
    elif locales_dict[message.chat.id] == 'az':
        await message.answer(help_msg_az, disable_web_page_preview=True)
@rate_limit(limit=5)
@dp.message_handler(commands=['help_group'], commands_prefix="/!@")
async def command_help_group(message: types.Message):
    if locales_dict[message.chat.id] == 'ru':
        await message.answer(help_group)
    elif locales_dict[message.chat.id] == 'az':
        await message.answer(help_group_az)

@rate_limit(limit=5)
@dp.message_handler(commands=['help_uni'], commands_prefix="/!@")
async def command_help_unibook(message: types.Message):
    if locales_dict[message.chat.id] == 'ru':
        await message.answer(help_unibook)
    elif locales_dict[message.chat.id] == 'az':
        await message.answer(help_unibook_az)

@rate_limit(limit=10)
@dp.message_handler(commands=['help'], commands_prefix="/!@")
async def command_help(message: types.Message):
    await message.reply(await _('<b><i>Используйте команды ниже для получения подробной информации:</i></b>\n\n/help_all - Все основные функции\n/help_group - Весь функционал для групп\n/help_uni - Весь функционал связанные с платформами университетов\n\nВ случае проблем, багов, ошибок, вопросов, предложений, писать сюда - @papayyg', locales_dict[message.chat.id]))
    if await BotDB.chats_exists(message.chat.id):
        await BotDB.chat_update(message.chat.id, message.from_user.first_name)
    else:
        await BotDB.add_chat(message.chat.id, message.from_user.first_name)
