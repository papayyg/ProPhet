<div align="center" id='readme-top'>
  <a href="https://github.com/othneildrew/Best-README-Template">
    <img src="https://i.ibb.co/qjgBq9M/photo-2023-04-08-01-37-55-removebg-preview.png" alt="Logo" width="120" height="120">
  </a>
  <h3 align="center">ProPhet 3</h3>
  <p align="center">
    Бот для упрощения и автоматизации процессов<br>
    <a href="https://t.me/natikbehruzbot">Telegram Link</a>
  </p>
</div>

## Описание
Telegram бот с исходным кодом, который имеет обширный функционал как для личного пользования, так и для групп. Основной функцией бота является парсинг электронных журналов университетов, включая расчет среднего балла, просмотр оценок, кредитов и загрузку файлов. 

## Что он умеет?
### 1. Основные функции
* `/start` - Приветственное сообщение, добавляет пользователя в БД и узнает язык.
* `/help` - Помощь по функционалу.
* `/ping` - Посмотреть состояние используемых серверов.
* `/lang` - Сменить язык.
* Отправьте `голосовое сообщение`, чтобы преобразовать его в текст.
* Обратитесь к боту `(бот,)` в начале ГС, чтобы отправить запрос GPT через голос.
* `/ts` *Текст\*_ - Перевод текста в речь.
* `/shazam` - Напишите ответом на аудио/видео/голосовое сообщение/видеосообщение, чтобы распознать музыку и получить аудио и ссылки.
* `/parkcinema` - Посмотреть список премьер в кинотеатрах ParkCinema.
* `/cinemaplus` - Посмотреть список премьер в кинотеатрах CinemaPlus.
* `/link` _\*ссылка\*_ - Вернет сокращенную ссылку.
* `/weather` _\*название города на англ. или русс.\*_ - Посмотреть погоду в Баку или указанном городе.
* `/translate` - Для перевода с русского на английский или с любого другого языка на русский.
* `/translateto` _\*код языка\*_ - Для перевода с любого языка на указанный ([Код](https://www.fincher.org/Utilities/CountryLanguageList.shtml) языка указывать в виде двух букв).
* _\*значение из валюты\*_ `to` _\*в валюту\*_ - Конвертировать валюту (Пример: 100 usd to azn).
* `/qbs` - Отправьте ответом на фото/стикер/текстовое сообщение, чтобы добавить стикер в пак чата.
* `/dbs` - Отправьте ответом на стикер из пака чата, чтобы удалить его из набора.
* Отправьте ссылку на _\*пост\*_  или _\*reel\*_  `Instagram`, чтобы скачать.
* Отправьте ссылку на `TikTok`, чтобы скачать _\*видео\*_  или _\*слайд-шоу\*_.
* Отправьте ссылку на `Youtube Shorts`, чтобы скачать _\*видео\*_.
* Отправьте ссылку на `Youtube` _\*видео\*_  до 5 минут, чтобы скачать его.
* Отправьте ссылку на _\*трек\*_  из `Яндекс.Музыка` для его скачивания.
* Напишите `бот, ` или `bot, ` и дальше после запятой интересующая вас тема или вопрос, чтоб отправить запрос боту GPT.
* Напишите `фото, ` или image, ` и дальше после запятой образ, который должен нарисовать ИИ.
* `/var` - Напишите ответом на фото, чтобы создать его вариации.
* `/real` _\*promt\*_ - Сгенерировать изображение используя модель Realistic Vision v2.
* `/dream` _\*promt\*_ - Сгенерировать изображение используя модель Dream Shaper 4.
* `/sound` - Отправьте ответом на видео, чтобы вырезать звук.
* `/c` _\*математическое выражение\*_ - Вычислить ответ для мат. выражения (`/c_help` для получения подробностей).
* `/coin` - Подбросить монетку.
* `/n` - Бот отвечает "Да" или "Нет".
* `/l` _\*от\*_ _\*до\*_ - Выбрать случайное число в промежутке.
* `/k` _\*Перечисление вариантов через пробел\*_ - Выбор случайного варианта из указанных.
* `Шар,` _\*Вопрос\*_ - Спросить у магического шара.

### 2. Функции для групп
* `/in` - Добавить себя в список участников группы.
* `/out` - Перестать быть участником группы.
* `/queer` - Включить ежедневный конкурс между участниками группы (Только для администратора).
* `/queerstats` - Посмотреть статистику ежедневного конкурса группы.
* `/all` - Отметить всех участников группы.
* `/mute`  _\*число\*_ _\*причина\*_ - Замутить пользователя на указанное время в минутах, можно и не указывать (/mute 10 мат).
* `/unmute` - Снять мут с пользователя.
* `/kick` - Исключить из группы.
* `/ban` - Заблокировать пользователя в группе.
* `/unban` - Разблокировать пользователя.
* `/purge` - Удалить все сообщения до указанного.

### 3. Функции электронных журналов
* `/auth` - Сохранить данные для авторизации в электронном журнале в БД.
* `/del` - Удалить сохраненные данные из базы.
* `/nb` - Посмотреть все НБ по всем предметам.
* `/journal` - Посмотреть итоговый журнал за семестр.
* `/gpa` - Посчитать средний балл за все семестры (Долгий процесс).
* `/gpas` - Посмотреть баллы и кредиты за каждый предмет всех семестров с выводом среднего балла (Долгий процесс).
* `/subjects` - Посмотреть всю информацию о каждом предмете, а также скачать файлы предмета (Лекции, силлабус и т.п.).

### Дополнения
* Префиксами команд могут служить: `/` `@` `!`
* Для работы некоторых функций (По типу GPT) в группах, нужно выдать права администратора боту.
* На данный момент доступны электронные журналы Unibook (ASOIU) и Empro (NAA).
* На некоторые команды работают алиасы, по типу: `вход` `нб` `журнал` `предметы`.

<p align="right">(<a href="#readme-top">Вернуться наверх</a>)</p>

## Установка
1. Клонируйте данный репозиторий:
```sh
git clone https://github.com/papayyg/ProPhet.git
```
2. Установите все библиотеки:
```sh
pip install -r requirements.txt
```
2. Создайте файл с названием `.env` в корне проекта и вставьте в нее все переменные среды из таблицы ниже в виде:
```sh
ПЕРЕМЕННАЯ=значение
```
| Переменные          | Описание                                                                                                                                             |
| ------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| API_TOKEN           | Токен бота полученный от [@BotFather](https://t.me/BotFather)                                                                                                                                          |
| DATABASE            | Название базы данных                                                                                                                                            |
| DB_HOST             | Адрес базы данных                                                                               |
| DB_USER             | Пользователь базы данных                                                                                                                                            |
| DB_PASS             | Пароль базы данных                                                                                                                                                 |
| OPENAI_API_KEY      | API ключ [OpenAI](https://openai.com/)                                                                                                                                           |
| OPEN_WEATHER        | API ключ [OpenWeather](https://openweathermap.org/)                                                                                                                                     |
| CURRENCY_API        | API ключ [Exchangerate](https://www.exchangerate-api.com/)                                                                             |
| YANDEX_TOKEN        | Токен аккаунта [Яндекс.Музыка](https://github.com/MarshalX/yandex-music-api/discussions/513)                                                                                                  |
| YOUTUBE_API         | API ключ [YouTubeAPI](https://developers.google.com/youtube/v3?hl=ru)                                              |
| CLIENT_ID           | ID клиента из [SpotifyAPI](https://developer.spotify.com/documentation/web-api)|
| CLIENT_SECRET       | Секретный ключ клиента из [SpotifyAPI](https://developer.spotify.com/documentation/web-api)|
| owner_id            | ID администратора|
| log_channel         | ID чата для логирования|
| bot_name            | Ник бота (@)|
| real                | Ссылка на Stable-diffusion с RealVision моделью|
| dream               | Ссылка на Stable-diffusion с DreamShapper моделью|

3. Установите ffmpeg с официального сайта:
* https://ffmpeg.org/download.html

4. Запустите `app.py`:
```sh
python app.py
```
<p align="right">(<a href="#readme-top">Вернуться наверх</a>)</p>

## Контакты

Аслан - [Telegram](https://t.me/papayyg) - aslan.mamedrzaev@gmail.com

Ссылка на проект: https://github.com/papayyg/ProPhet

<p align="right">(<a href="#readme-top">Вернуться наверх</a>)</p>



