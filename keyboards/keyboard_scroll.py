from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from API_requests import yandex_kp_api
from loader import bot
# from bases.SQLite_func import *
from bases.cheking_user_info import *
from bases.get_user_info import *
from bases.set_user_info import *
from bases.remove_user_info import *
import datetime
from keyboards.key_menu import key_menu


def keyboard_scroll(user_id: int, active_number: int = 0, lenn: int = 20, keyboard_mode: str = 'base'):
    """ 
    Создаем клавиатуру для навигации по результату 
    
    Аргументы:
        active_number (int): активная кнопка, кнопка которая должна быть помечена
        user_id (int): id пользователя
        lenn (int): кол-во кнопок на клавиатуре
        keyboard_mode (str): режим клавиатуры ['base', 'favourites']
    
    Вывод:
        (InlineKeyboardMarkup): клавиатура
    """
    
        
    if keyboard_mode == 'base':
        data: list = db_get_films_data(user_id=user_id)['docs']
        callback_add_favourites = f'add_favourites:{active_number}'
        callback_remove_favourites = f'remove_favourites:{active_number}'
        callback_add_watched = f'add_watched:{active_number}'
        callback_remove_watched = f'remove_watched:{active_number}'
    elif keyboard_mode == 'favourites':
        data: list = db_get_films_favourites(user_id=user_id)['favourites']
        callback_remove_favourites = f'remove_favourites_2:{active_number}'
        callback_add_watched = f'add_watched_2:{active_number}'
        callback_remove_watched = f'remove_watched_2:{active_number}'
    
    native_len_request = len(data)
    keyboard = InlineKeyboardMarkup(row_width=5)
    film_id = data[active_number]['id']
    buttons_list = list()
    watched_bef = db_checking_film_in_watched(user_id=user_id, film_id=film_id)
    
    if native_len_request < lenn:
        final_lenn = native_len_request
    else:
        final_lenn = lenn
    
    for num_but in range(final_lenn):
        text_button = f'< {num_but + 1} >' if active_number == num_but else f'{num_but + 1}'
        text_callback = (f'button:{num_but}:{final_lenn}' 
                         if keyboard_mode == 'base' else 
                         f'button_2:{num_but}:{final_lenn}')
        button = InlineKeyboardButton(text=text_button, callback_data=text_callback)
        buttons_list.append(button)
    
    if keyboard_mode == 'favourites' or db_checking_film_in_favourites(user_id=user_id, film_id=film_id):
        button_favourites = InlineKeyboardButton(text='Убрать из избранного', 
                                                 callback_data=callback_remove_favourites + f':{final_lenn}')
    else:
        button_favourites = InlineKeyboardButton(text='Добавить в избранное', 
                                                 callback_data=callback_add_favourites + f':{final_lenn}')
    
    if watched_bef:
        watched_button = InlineKeyboardButton(text='Отметить непросмотренным', 
                                              callback_data=callback_remove_watched + f':{final_lenn}')
    else:
        watched_button = InlineKeyboardButton(text='Отметить просмотренным', 
                                              callback_data=callback_add_watched + f':{final_lenn}')

    keyboard.add(button_favourites, watched_button)
    keyboard.add(*buttons_list)
        
    return keyboard


@bot.callback_query_handler(func=lambda call: call.data.split(':')[0] in ['button', 'button_2'])
def callback_inline(call) -> None:
    """ Заменяем результат поиска по названию фильма по нажатию на кнопку """
    
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    calldata_list = call.data.split(':')
    button_mode = calldata_list[0]
    active_number = int(calldata_list[1])
    final_lenn = int(calldata_list[2])
    
    if button_mode == 'button':
        keyboard = keyboard_scroll(user_id=user_id, active_number=active_number, lenn=final_lenn)
        media: tuple = yandex_kp_api.see_result(data=db_get_films_data(user_id=user_id),  
                                                number=active_number,
                                                user_id=user_id)
    else:
        keyboard = keyboard_scroll(user_id=user_id, 
                                   active_number=active_number, 
                                   lenn=final_lenn, 
                                   keyboard_mode='favourites')
        
        media: tuple = yandex_kp_api.see_result(data=db_get_films_favourites(user_id=user_id),
                                                number=active_number,
                                                name_param="favourites",
                                                user_id=call.from_user.id)

    bot.edit_message_media(media=InputMediaPhoto(media[0]), 
                           chat_id=chat_id, 
                           message_id=message_id)
    
    bot.edit_message_caption(
        caption=media[1], 
        chat_id=chat_id, 
        message_id=message_id, 
        reply_markup=keyboard)
    
    
@bot.callback_query_handler(func=lambda call: (call.data.split(':'))[0] == 'add_favourites')
def add_favourites(call):
    """ Добавляем фильм в избранное """
    
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    calldata_list = call.data.split(':')
    active_number = int(calldata_list[1])
    final_lenn = int(calldata_list[2])
    film_data: dict = db_get_films_data(user_id=user_id)['docs'][active_number]
    film_name = film_data['name']
    date_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    db_set_film_in_favorites(user_id=user_id,film_data=film_data)
    bot.edit_message_reply_markup(chat_id=chat_id,
                                  message_id=message_id,
                                  reply_markup=keyboard_scroll(lenn=final_lenn, 
                                                               active_number=active_number, 
                                                               user_id=user_id))
    
    db_set_action_history(user_id=user_id, 
                          text=f"{date_now} - Добавляем фильм '{film_name}' в избранное")


@bot.callback_query_handler(func=lambda call: (call.data.split(':'))[0] in 
                            ['remove_favourites', 'remove_favourites_2'])
def remove_favourites(call):
    """ Убираем фильм из избранного """
    
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    calldata_list = call.data.split(':')
    button_mode = calldata_list[0]
    active_number = int(calldata_list[1])
    final_lenn = int(calldata_list[2])
    date_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if button_mode == 'remove_favourites':
        data_films: dict = db_get_films_data(user_id=user_id)
        film_name = data_films['docs'][active_number]['name']
        film_id = data_films['docs'][active_number]['id']
        
        db_remove_film_in_favorites(user_id=user_id, film_id=film_id)
        
        keyboard = keyboard_scroll(user_id=user_id, active_number=active_number, lenn=final_lenn)
        
        bot.edit_message_reply_markup(chat_id=chat_id,
                                      message_id=message_id,
                                      reply_markup=keyboard)
        
    elif button_mode == 'remove_favourites_2':
        data_films: dict = db_get_films_favourites(user_id=user_id)
        film_name = data_films['favourites'][active_number]['name']
        film_id = data_films['favourites'][active_number]['id']
        
        db_remove_film_in_favorites(user_id=user_id, film_id=film_id)
        
        data_films = db_get_films_favourites(user_id=user_id)
        
        if len(data_films["favourites"]) == 0:
            bot.delete_message(chat_id=chat_id, message_id=message_id)
            bot.send_message(chat_id=call.message.chat.id,
                             text='Ваш список избранного пуст',
                             reply_markup=key_menu())
            
        elif len(data_films['favourites']) != 0:

            if active_number > 0:
                active_number -= 1
            
            keyboard = keyboard_scroll(user_id=user_id, 
                                       active_number=active_number, 
                                       lenn=final_lenn, 
                                       keyboard_mode='favourites')
            
            media: tuple = yandex_kp_api.see_result(data=data_films,
                                                    number=active_number,
                                                    name_param="favourites",
                                                    user_id=user_id)
            
            bot.edit_message_media(media=InputMediaPhoto(media[0]), 
                                   chat_id=chat_id, 
                                   message_id=message_id)
            
            bot.edit_message_caption(caption=media[1], 
                                     chat_id=chat_id, 
                                     message_id=message_id, 
                                     reply_markup=keyboard)
    
    db_set_action_history(user_id=user_id, text=f"{date_now} - Убираем '{film_name}' из избранного")

    
@bot.callback_query_handler(func=lambda call: (call.data.split(':'))[0] 
                            in ['add_watched', 'add_watched_2'])
def add_in_watched(call):
    """ Добавляет фильм в просмотренные """
    
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    calldata_list = call.data.split(':')
    button_mode = calldata_list[0]
    active_number = int(calldata_list[1])
    final_lenn = int(calldata_list[2])
    date_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if button_mode == 'add_watched':
        films_data = db_get_films_data(user_id=call.from_user.id)
        film_id = films_data['docs'][active_number]['id']
        film_name = films_data['docs'][active_number]['name']
        
        db_set_film_in_watched(user_id=user_id, film_id=film_id)
        
        keyboard = keyboard_scroll(user_id=user_id, active_number=active_number, lenn=final_lenn)
        media = yandex_kp_api.see_result(data=films_data,
                                         number=active_number,
                                         user_id=user_id)
        
        bot.edit_message_caption(caption=media[1], 
                                 chat_id=call.message.chat.id, 
                                 message_id=call.message.message_id, 
                                 reply_markup=keyboard)
        
    elif button_mode == 'add_watched_2':
        films_data = db_get_films_favourites(user_id=user_id)
        film_id = films_data['favourites'][active_number]['id']
        film_name = films_data['favourites'][active_number]['name']
        
        db_set_film_in_watched(user_id=user_id, film_id=film_id)
        
        keyboard = keyboard_scroll(lenn=final_lenn,
                                   active_number=active_number,
                                   user_id=user_id,
                                   keyboard_mode='favourites')

        media = yandex_kp_api.see_result(data=films_data,
                                         number=active_number,
                                         user_id=user_id,
                                         name_param="favourites")
        
        bot.edit_message_caption(caption=media[1], 
                                 chat_id=chat_id, 
                                 message_id=message_id, 
                                 reply_markup=keyboard)
        
    db_set_action_history(user_id=user_id, text=f"{date_now} - Отмечаем '{film_name}' просмотренным")
        

@bot.callback_query_handler(func=lambda call: (call.data.split(':'))[0] 
                            in ['remove_watched', 'remove_watched_2'])
def remove_in_watched(call):
    """ Убираем статус просмотренно """
    
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    calldata_list = call.data.split(':')
    button_mode = calldata_list[0]
    active_number = int(calldata_list[1])
    final_lenn = int(calldata_list[2])
    date_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if button_mode == 'remove_watched':
        films_data = db_get_films_data(user_id=user_id)
        film_id = films_data['docs'][active_number]['id']
        film_name = films_data['docs'][active_number]['name']
        
        db_remove_film_in_watched(user_id=user_id, film_id=film_id)
        
        keyboard = keyboard_scroll(lenn=final_lenn,
                                   active_number=active_number,
                                   user_id=user_id)

        media = yandex_kp_api.see_result(data=films_data,
                                         number=active_number,
                                         user_id=user_id)
        
        bot.edit_message_caption(caption=media[1], 
                                 chat_id=chat_id, 
                                 message_id=message_id, 
                                 reply_markup=keyboard)

    else:
        films_data = db_get_films_favourites(user_id=user_id)
        film_id = films_data['favourites'][active_number]['id']
        film_name = films_data['favourites'][active_number]['name']
        
        db_remove_film_in_watched(user_id=user_id, film_id=film_id)
        
        keyboard = keyboard_scroll(lenn=final_lenn,
                                   active_number=active_number,
                                   user_id=user_id,
                                   keyboard_mode='favourites')
        
        media = yandex_kp_api.see_result(data=films_data,
                                         number=active_number,
                                         user_id=user_id,
                                         name_param="favourites")
        bot.edit_message_caption(caption=media[1], 
                                 chat_id=chat_id, 
                                 message_id=message_id, 
                                 reply_markup=keyboard)
        
    db_set_action_history(user_id=user_id, text=f"{date_now} - Отмечаем '{film_name}' непросмотренным")
