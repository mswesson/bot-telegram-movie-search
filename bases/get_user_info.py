from bases.models import User
import json
from loader import bot
from typing import Optional


def db_get_films_data(user_id: int) -> Optional[dict]:
    """ Выдает словарь с фильмами """
    user = User.get_or_none(User.user_id == user_id)
    
    if user:
        data = json.loads(user.data)
        return data
    else:
        print(f'{'-' * 10} Ошибка в функции db_get_films_data: пользователь с user_id {user_id} не найден')
        
        
def db_get_search_param(user_id: int, param: str) -> Optional[any]:
    """ Выдает параметр поиска """
    user: User = User.get(User.user_id == user_id)
    
    if user:
        params_search: dict = json.loads(user.search_param)
        param_search = params_search.get(param, None)
        if param_search:
            return param_search
        else:
            print(f'{'-' * 10} Ошибка в функции db_get_search_param: пользователь с user_id {user_id} не найден')


def db_get_films_favourites(user_id: int) -> Optional[dict]:
    """ Выдает словарь с фильмами, которые находятся в избранном """

    user: User = User.get_or_none(User.user_id == user_id)
    if user:
        data: dict = json.loads(user.favourites)
        return data
    else:
        print(f'{'-' * 10} Ошибка в функции db_get_films_favourites: пользователь с user_id {user_id} не найден')


def db_get_history(user_id: int) -> Optional[list]:
    """ Выдает список истории """
    user: User = User.get_or_none(User.user_id == user_id)
    
    if user:
        cur_history: dict = json.loads(user.history)
        cur_history_list: list = cur_history["history_search"]
        return cur_history_list
    else:
        print(f'{'-' * 10} Ошибка в функции db_get_history: пользователь с user_id {user_id} не найден')