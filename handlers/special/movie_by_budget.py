from telebot.types import Message, ReplyKeyboardRemove
from loader import bot
from states.movie_budget import MovieSearch
from keyboards.keyboard_scroll import keyboard_scroll
from keyboards.key_genres import keyboard_genres, GENRES_LIST
from keyboards.key_menu import key_menu, key_back
from API_requests import yandex_kp_api
from bases.set_user_info import db_set_action_history, db_set_films_data, db_set_search_param
from bases.get_user_info import db_get_films_data, db_get_search_param
from bases.cheking_user_info import db_checking_user
from bases.remove_user_info import db_remove_search_param
import datetime


@bot.message_handler(commands=['movie_by_budget'])
def movie_by_budget(message: Message) -> None:
    """ 1. Запрашиваем бюджет """
    
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    if not db_checking_user(user_id=user_id):
        bot.send_message(chat_id=chat_id, text=('Вы еще не зарегестрировались. '
                                                'Введите команду /start для автоматической регистрации'),
                         reply_markup=key_menu())
        return
    
    bot.send_message(chat_id=chat_id, 
                     text=('Режим "Поиск по бюджету" активирован.\n\n'
                           'Введите диапазон бюджета (пример: 1000 - 6666666)'),
                     reply_markup=key_back())
    
    bot.set_state(user_id=user_id, state=MovieSearch.search_budget)
    
    
@bot.message_handler(state=MovieSearch.search_budget,
                     func=lambda message: message.text != 'Вернуться в главное меню')
def movie_by_budget_2(message: Message) -> None:
    """ 2. Обрабатываем бюджет, запрашиваем жанр """
    
    chat_id = message.chat.id
    user_id = message.from_user.id
    user_text: str = message.text.replace(' ', '')
    checking_1: bool = user_text.replace('-', '').isdigit()
    checking_2: bool = len(user_text.split('-')) in [1, 2]
    if checking_2 and len(user_text.split('-')) == 1:
        checking_3: bool = user_text.split('-')[0].isdigit() and 0 <= float(user_text.split('-')[0])
        if checking_3:
            checking_4: bool = True
    else:
        checking_3: bool = user_text.split('-')[0].isdigit() and 0 <= float(user_text.split('-')[0]) and 0 <= float(user_text.split('-')[1])
        if checking_3:
            checking_4: bool = float(user_text.split('-')[0]) < float(user_text.split('-')[1])
    
    if checking_1 and checking_2 and checking_3 and checking_4:
        
        bot.send_message(chat_id=chat_id, text=f'Теперь выберете жанр', reply_markup=keyboard_genres())
        db_set_search_param(user_id=user_id, param='budget', value=user_text)
        bot.set_state(user_id=user_id, state=MovieSearch.search_budget_genres)
        
    else:
        bot.send_message(chat_id=chat_id,
                         text=(f'Ваш запрос "{user_text}" не удовлетворяет критериям диапазона:\n'
                               '- только цифры\n'
                               '- одно, либо два значения\n'
                               '- значения должны быть больше или равны 0\n'
                               '- при диапазоне второе значение должно быть больше первого'))


@bot.message_handler(state=MovieSearch.search_budget_genres,
                     func=lambda message: message.text != 'Вернуться в главное меню')
def movie_by_budget_3(message):
    """ 3. Обрабатываем жанр, выводим результат """
    
    chat_id = message.chat.id
    user_id = message.from_user.id
    date_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if not message.text.lower() in GENRES_LIST:
        bot.send_message(chat_id=chat_id,
                         text='Выберите жанр из меню, либо введите сами без спец символов и пробелов')
        return
        
    db_set_search_param(user_id=user_id, param='genres', value=message.text.lower())
    
    budget = db_get_search_param(user_id=user_id, param='budget')
    genres = db_get_search_param(user_id=user_id, param='genres')
    server_response = yandex_kp_api.yandex_requests(budget=budget, genres=genres)
    
    db_remove_search_param(user_id=user_id)
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
    
    bot.send_photo(chat_id=chat_id, 
                    photo=media[0], 
                    caption=media[1], 
                    reply_markup=keyboard)
    bot.send_message(chat_id=chat_id, 
                        text=('Режим "Поиск по бюджету" завершен.\n\n'
                            'Воспользуйтесь меню, для дальнейшего взаимодействия.'),
                        reply_markup=key_menu())
    
    bot.delete_state(user_id=user_id, chat_id=chat_id)
    
    db_set_action_history(user_id=user_id, 
                          text=f"{date_now} - Поиск по бюджету: бюджет '{budget}', жанр '{genres}'")
