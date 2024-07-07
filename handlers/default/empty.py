from telebot.types import Message
from loader import bot

@bot.message_handler()
def start_message(message: Message):
    """ Сообщение при необработанном запросе """
    
    chat_id = message.chat.id
    user_name = message.from_user.username
    
    print(f'Пользователь {user_name} входит в "empty"')
    
    bot.send_message(chat_id=chat_id, text='Я не понимаю, попробуй /start')