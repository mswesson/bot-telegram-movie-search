from telebot.types import Message
from loader import bot
from keyboards.keyboard_scroll import keyboard_scroll
from API_requests import yandex_kp_api
from bases.cheking_user_info import db_checking_user
from bases.get_user_info import db_get_films_favourites
from bases.set_user_info import db_set_action_history
import datetime


@bot.message_handler(commands=['favorites'])
def favorites(message: Message) -> None:
    """ Выводим список избранных фильмов """
    
    user_id = message.from_user.id
    chat_id = message.chat.id
    data_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if not db_checking_user(user_id=user_id):
        bot.send_message(chat_id=chat_id, text=('Вы еще не зарегестрировались. '
                                                'Введите команду /start для автоматической регистрации'))
        return
    
    data_favourites_films: dict = db_get_films_favourites(user_id=user_id)
    favorite_films_counter: int = len(data_favourites_films['favourites'])
    
    if not favorite_films_counter:
        bot.send_message(chat_id=chat_id, text='Ваш список избранного пуст')
        return
    
    keyboard = keyboard_scroll(user_id=user_id, keyboard_mode='favourites')  
    media: tuple = yandex_kp_api.see_result(data=data_favourites_films,
                                            user_id=user_id,
                                            name_param="favourites")
    
    bot.send_message(chat_id=chat_id,text='Переходим в ваш список избранного')
    bot.send_photo(chat_id=chat_id, 
                   photo=media[0], 
                   caption=media[1], 
                   reply_markup=keyboard)
    bot.send_message(chat_id=chat_id, text='Воспользуйтесь меню, для дальнейшего взаимодействия.')
    db_set_action_history(user_id=user_id, text=f"{data_now} - Переходим в раздел избранное")
