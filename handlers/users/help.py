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
/sz - Напишите ответом на аудио/видео/голосовое сообщение/видеосообщение, чтобы распознать музыку (Шазам)

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
<i>Отправьте ссылку на <b>TikTok</b>, чтобы скачать видео или слайд-шоу</i>
<i>Отправьте ссылку на <b>Youtube Shorts</b>, чтобы скачать видео</i>
<i>Отправьте ссылку на <b>Youtube видео</b> до 3.5 минут, чтобы скачать его</i>
<i>Отправьте ссылку на трек из <b>Яндекс.Музыка</b> для его скачивания</i>

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

help_msg_az = '''<i><b>Bütün bot funksiyaları</b></i>
<b>Əmr prefiksləri: / @ !</b>

/n - Bot "Bəli" və ya "Xeyr" cavabı verir
/l <i><b>*dən*</b></i> <i><b>*qədər*</b></i> - Aralıqda təsadüfi bir nömrənin seçimi
/k <i><b>*Boşluqlarla ayrılmış seçimlərin siyahısı*</b></i> - Siyahıdakı seçimlərdən birini təsadüfi seçmək
/coin - Bot bir sikkə atır
/c <i><b>*riyaziyyat ifadəsi*</b></i> - Riyaziyyat ifadəsi üçün cavabı hesablamaq (ətraflı məlumat üçün/c_help)
/sound - Videodan səsi kəsmək üçün video mesajına cavab verin
Kürə, <i>"Sual"</i> - Sehrli kürədən soruşmaq

<i>Səsli mesajın yazılı mətnə çevirməsi</i>
<i>GPT-e sorgu gondermek ucun sesli mesajin evvelinde bota muraciyyet edin (bot,) </i>
/ts <i><b>*Mətn*</b></i>- Yazılı mesajın səsli mesaja çevrilməsi
/sz - Musiqini tanımaq üçün audio/video/səs/video mesaja cavab yazın (Shazam)

/parkcinema - ParkCinema kinoteatrlarında premyeraların siyahısına baxmaq
/cinemaplus - CinemaPlus kinoteatrlarında premyeraların siyahısına baxmaq

/link <b>*link*</b> - Qısaldılmış linki qaytarır
/weather <i><b>İngiliscə şəhər adı</b></i> - Bakıda və ya müəyyən şəhərdə havaya baxmaq
/translate - Rus dilindən ingilis dilinə və ya hər hansı digər dildən rus dilinə tərcümə
/translateto <i><b>dil kodu</b></i> - İstənilən dildən göstərilən dilə tərcümə etmək üçün (<a href="https://www.fincher.org/Utilities/CountryLanguageList.shtml" >Kod </a> dilləri iki hərf kimi göstərilməlidir)
<i>dəyər</i> <b>valyutadan</b> to <b>valyutaya</b> - Valyutanı çevir (Məsələn: 100 usd to azn)

/qbs - Stikeri çat paketinə əlavə etmək üçün foto/stiker/mətn mesajına cavab verin
/dbs - Stikeri dəstdən çıxarmaq üçün bu əmri stikerə cavabla göndərin

<i><b>Instagram</b> foto və ya video yükləmək üçün link göndərin</i>
<i><b>TikTok</b>-dan video və ya slayd şousunu yükləmək üçün link göndərin</i>
<i><b>Youtube Shorts</b>-dan video yükləmək üçün link göndərin</i>
<i><b>YouTube-dan video</b> (3.5 dəqiqəyə qədər) yükləmək üçün link göndərin</i>
<i><b>Yandex.Music</b>-dən musiqiyi yükləmək üçün link göndərin</i>

GPT botuna sorğu göndərmək üçün əvvəlcə yazın bot, (bot, ) və sonra vergüldən sonra maraqlandığınız mövzunu və ya sualı daxil edin
image yazın və sonra AI-nin çəkməli olduğu şəkli vergüldən sonra təsvir edin (image, )
Foto və ya şəkil yazın, sonra vergüldən sonra AI-nin çəkməli olduğu şəkli yazın.
/var - Fotonun variasiyalarını yaratmaq üçün ona cavab yazın

<i>Test funksiyaları, işləməyə bilər</i>
/real <b>*promt*</b> - Realistic Vision v2 modelindən istifadə edərək şəkil yaratmaq
/dream <b>*promt*</b> - Dream Shaper 4 modelindən istifadə edərək şəkil yaratmaq

/start - Salam mesajı
/help - Funksionallıqla bağlı yardım
/ping - Serverlərin vəziyyətinə baxmaq
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
