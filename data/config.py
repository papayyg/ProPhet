import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv("API_TOKEN"))
TEST_TOKEN = str(os.getenv("TEST_TOKEN"))

DATABASE=str(os.getenv("DATABASE"))
DB_HOST=str(os.getenv("DB_HOST"))
DB_USER=str(os.getenv("DB_USER"))
DB_PASS=str(os.getenv("DB_PASS"))

OPENAI_API_KEY=str(os.getenv("OPENAI_API_KEY"))
OPEN_WEATHER=str(os.getenv("OPEN_WEATHER"))
CURRENCY_API=str(os.getenv("CURRENCY_API"))
YANDEX_TOKEN=str(os.getenv("YANDEX_TOKEN"))
YOUTUBE_API=str(os.getenv("YOUTUBE_API"))

owner_id = int(os.getenv("owner_id"))
log_channel = int(os.getenv("log_channel"))
bot_name=str(os.getenv('bot_name'))

real=str(os.getenv("real"))
dream=str(os.getenv("dream"))

