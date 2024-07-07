from dotenv import load_dotenv
import os

load_dotenv()

KINOPOISK_API = os.getenv('KINOPOISK_API')  # Kinopoisk API key
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')  # Telegram bot token

