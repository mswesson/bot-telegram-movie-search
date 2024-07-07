from telebot.types import Message
from loader import bot
from states.movie_search import MovieSearch
from keyboards.keyboard_scroll import keyboard_scroll
from keyboards.key_menu import key_menu, key_back
from API_requests import yandex_kp_api
from bases.set_user_info import db_set_action_history, db_set_films_data
from bases.get_user_info import db_get_films_data
from bases.cheking_user_info import db_checking_user
import datetime


@bot.message_handler(commands=['movie_search'])
def movie_search(message: Message):
    """ 1. Начинаем поиск фильма по имени. Просим ввести название фильма """
    
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    if not db_checking_user(user_id=user_id):
        bot.send_message(chat_id=chat_id, text=('Вы еще не зарегестрировались. '
                                                'Введите команду /start для автоматической регистрации'),
                         reply_markup=key_menu())
        return

    bot.send_message(chat_id=chat_id, 
                     text='Режим "Поиск по названию" активирован.\n\n''Введите название фильма',
                     reply_markup=key_back())

    bot.set_state(user_id=user_id, 
                  state=MovieSearch.search, 
                  chat_id=chat_id)


@bot.message_handler(state=MovieSearch.search, 
                     func=lambda message: message.text != 'Вернуться в главное меню')
def movie_search_2(message: Message) -> None:
    """ 2. Обрабатываем название фильма и выводим результат """
    
    chat_id = message.chat.id
    user_id = message.from_user.id
    film_name = message.text.strip()
    date_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    server_response = yandex_kp_api.yandex_requests(query=film_name)

    if not server_response:
        bot.send_message(chat_id=chat_id, 
                         text='Нет ответа от сервера. Попробуйте позже',
                         reply_markup=key_menu())
        bot.delete_state(user_id=user_id, chat_id=chat_id)
        return
    
    elif server_response['total_2'] == 0:
        bot.send_message(chat_id=chat_id, 
                         text='Ни одного фильма с такими параметрами не было найдено, попробуйте снова',
                         reply_markup=key_menu())
        bot.delete_state(user_id=user_id, chat_id=chat_id)
        return
    
    db_set_films_data(user_id=user_id, data=server_response)
    
    films_data = db_get_films_data(user_id=user_id)
    media = yandex_kp_api.see_result(data=films_data, user_id=user_id)     
    keyboard = keyboard_scroll(user_id=user_id)
    
    bot.send_photo(chat_id=chat_id, 
                   photo=media[0], 
                   caption=media[1], 
                   reply_markup=keyboard)   

    bot.send_message(chat_id=chat_id, 
                     text=('Режим "Поиск по названию" завершен.\n\n'
                           'Воспользуйтесь меню, для дальнейшего взаимодействия.'),
                     reply_markup=key_menu())
    
    bot.delete_state(user_id=user_id, chat_id=chat_id)
    db_set_action_history(user_id=user_id, text=f"{date_now} - Поиск по названию: название '{film_name}'")
