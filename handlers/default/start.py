from telebot.types import Message
from loader import bot
from keyboards.key_menu import key_menu
from bases.set_user_info import db_set_new_user, db_set_action_history
import datetime

@bot.message_handler(commands=['start'])
def start(message: Message):
    """ Выводит сообщение приветствия и пытается добавить нового пользователя в БД """
    
    chat_id = message.chat.id
    user_id = message.from_user.id
    user_name = message.from_user.username
    data_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full_name = message.from_user.full_name
    
    if full_name is None:
        full_name = 'пользователь'
    
    bot.send_message(chat_id=chat_id, 
                     text=(f'Привет, {full_name}\n\n'
                           'Я помощник по поиску фильмов. Я могу искать фильмы по названию, '
                           'рейтигу и жанру, а так же по бюджету и жанру. '
                           'Могу показать тебе исторю твоих запросов. Ещё умею сохранять фильмы в избранное \n'
                           'и отмечать просмотренными.\n\n'
                           'Чтобы начать поиск воспользуйтесь кнопками меню. '
                           'Более детальная информация '
                           'находится в разделе помощь /help'),
                     reply_markup=key_menu())
    
    db_set_new_user(user_id=user_id, user_name=user_name)
    db_set_action_history(user_id=user_id, text=f"{data_now} - Переходим на стартовую страницу")
