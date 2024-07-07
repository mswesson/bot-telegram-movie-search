from telebot.types import Message
from loader import bot
# from bases.SQLite_func import *
from bases.get_user_info import db_get_history
from bases.cheking_user_info import db_checking_user


@bot.message_handler(commands=['history'])
def history(message: Message) -> None:
    """ Выводит историю использования бота на экран """

    chat_id = message.chat.id
    user_id = message.from_user.id

    if not db_checking_user(user_id=user_id):
        bot.send_message(chat_id=chat_id, text=('Вы еще не зарегестрировались. '
                                                'Введите команду /start для автоматической регистрации'))
        return

    history_data = db_get_history(user_id=user_id)
    text: str = ''
    for line in history_data:
        text += line + '\n\n'
    bot.send_message(chat_id=chat_id,
                     text='История действий:\n\n' + text)
