from telebot.types import Message, ReplyKeyboardRemove
from loader import bot
from states.movie_by_rating import MovieRating
from keyboards.keyboard_scroll import keyboard_scroll
from keyboards.key_genres import keyboard_genres, GENRES_LIST
from keyboards.key_menu import key_menu, key_back
from keyboards.key_platform import keyboard_platform
from API_requests import yandex_kp_api
from keyboards.key_menu import key_back, key_menu
from bases.cheking_user_info import db_checking_user
from bases.set_user_info import db_set_search_param, db_set_films_data, db_set_action_history
from bases.get_user_info import db_get_search_param, db_get_films_data
from bases.remove_user_info import db_remove_search_param
import datetime

@bot.message_handler(commands=['movie_by_rating'])
def movie_by_rating(message: Message) -> None:
    """ 1. Запрашиваем платформу """
    
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    if not db_checking_user(user_id=user_id):
        bot.send_message(chat_id=chat_id, text=('Вы еще не зарегестрировались. '
                                                'Введите команду /start для автоматической регистрации'),
                         reply_markup=key_menu())
        return
    
    bot.send_message(chat_id=chat_id, 
                     text=('Режим "Поиск по рейтингу" активирован.\n\n'
                           'На какой платформе будем искать?'), 
                     reply_markup=keyboard_platform())
    
    bot.set_state(user_id=user_id, state=MovieRating.search_platform, chat_id=chat_id)
        
    
@bot.message_handler(state=MovieRating.search_platform, 
                     func=lambda message: message.text != 'Вернуться в главное меню')
def movie_by_rating_2(message):
    """ 2. Обрабатываем платформу, запрашиваем рейтинг """
    
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    if message.text == 'Кинопоиск':
        value = 'rating.kp'
        bot.send_message(chat_id=chat_id, 
                         text=('Начинаем поиск в Кинопоиск\n\n'
                               'Введите рейтинг для поиска. Пример: 7.1, 9, 7.2-10'),
                         reply_markup=key_back())  
             
    elif message.text == 'IMDb':
        value = 'rating.imdb'
        bot.send_message(chat_id=chat_id, 
                         text=('Начинаем поиск в IMDb\n\n'
                               'Введите рейтинг для поиска. Пример: 7.1, 9, 7.2-10'),
                         reply_markup=key_back())
    else:
        bot.send_message(chat_id=chat_id, text='Платформа введена некорректно')
        return
    
    db_set_search_param(user_id=user_id, param='platform', value=value)    
    bot.set_state(user_id=user_id, state=MovieRating.search_rating)

    
@bot.message_handler(state=MovieRating.search_rating,
                     func=lambda message: message.text != 'Вернуться в главное меню')
def movie_by_rating_3(message: Message):
    """ 3. Обрабатываем рейтинг, запрашиваем жанр """
    
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    user_text: str = message.text.replace(' ', '')
    checking_1: bool = user_text.replace('-', '').isdigit()
    checking_2: bool = len(user_text.split('-')) in [1, 2]
    if checking_2 and len(user_text.split('-')) == 1:
        checking_3: bool = user_text.split('-')[0].isdigit() and 0 <= float(user_text.split('-')[0]) <= 10
        checking_4: bool = True
    else:
        checking_3: bool = user_text.split('-')[0].isdigit() and 0 <= float(user_text.split('-')[0]) <= 10 and 0 <= float(user_text.split('-')[1]) <= 10
        if checking_3:
            checking_4: bool = float(user_text.split('-')[0]) < float(user_text.split('-')[1])
    
    if checking_1 and checking_2 and checking_3 and checking_4:
        
        db_set_search_param(user_id=user_id, param='rating', value=user_text)
        bot.set_state(user_id=user_id, state=MovieRating.search_genres, chat_id=chat_id)
        bot.send_message(chat_id=chat_id, text='Теперь выберете жанр', reply_markup=keyboard_genres())
        
    else:
        bot.send_message(chat_id=chat_id,
                         text=(f'Ваш запрос "{user_text}" '
                               'не удовлетворяет критериям диапазона:\n'
                               '- только цифры\n'
                               '- одно, либо два значения через дефис\n'
                               '- значения должны быть от 0 до 10\n'
                               '- при диапазоне второе значение должно быть больше первого'))
        

@bot.message_handler(state=MovieRating.search_genres,
                     func=lambda message: message.text != 'Вернуться в главное меню')
def movie_by_rating_4(message):
    """ 4. Обрабатываем жанр, выводим результат """
    
    chat_id = message.chat.id
    user_id = message.from_user.id
    date_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if not message.text.lower() in GENRES_LIST:        
        bot.send_message(chat_id=chat_id,
                         text='Выберите жанр из меню, либо введите сами без спец символов и пробелов')
        return
        
    db_set_search_param(user_id=user_id, param='genres', value=message.text.lower())
    
    platform = db_get_search_param(user_id=user_id, param='platform')
    rating = db_get_search_param(user_id=user_id, param='rating') 
    genres = db_get_search_param(user_id=user_id, param='genres')
    server_response = yandex_kp_api.yandex_requests(platform=platform, rating=rating, genres=genres)
    
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
        db_remove_search_param(user_id=user_id)
        return

    db_set_films_data(user_id=user_id, data=server_response)
    
    films_data = db_get_films_data(user_id=user_id)
    media = yandex_kp_api.see_result(data=films_data, user_id=user_id)        
    keyboard = keyboard_scroll(user_id=user_id)
    
    bot.send_photo(chat_id=chat_id, photo=media[0], caption=media[1], reply_markup=keyboard)
    bot.send_message(chat_id=chat_id, 
                        text=('Режим "Поиск по рейтингу" завершен.\n\n'
                              'Воспользуйтесь меню, для дальнейшего взаимодействия.'),
                        reply_markup=key_menu())
    
    db_remove_search_param(user_id=user_id)
    bot.delete_state(user_id=user_id,chat_id=chat_id)
    
    if platform == 'rating.kp':
        platform_name = 'кинопоиск'
    else:
        platform_name = 'imdb'
        
    db_set_action_history(user_id=user_id,
                            text=(f"{date_now} - Поиск по рейтингу: платформа '{platform_name}', "
                                  f"рейтинг '{rating}', жанр '{genres}'"))
