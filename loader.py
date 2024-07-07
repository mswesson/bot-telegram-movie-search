import telebot
from config_data import config


bot = telebot.TeleBot(config.TELEGRAM_TOKEN)
