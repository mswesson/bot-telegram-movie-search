# from peewee import *
from bases.models import User
import json
from loader import bot


def db_set_new_user(user_id: int, user_name: str) -> None:
    """ Создает нового пользователя если такого еще нет """
    user = User.get_or_none(User.user_id == user_id)

    if not user:
        user = User(user_id=user_id,
                    user_name=user_name if user_name else 'NoName',
                    data='None',
                    search_param="{}",
                    favourites='{"favourites": []}',
                    watched_movies='{}',
                    history='{"history_search": []}')
        user.save()
        print(f'{'-' * 10} Пользователь {user_name} теперь зарегестрирован')
    else:
        print(f'{'-' * 10} Пользователь {user_name} уже зарегестрирован')


def db_set_films_data(user_id: int, data: dict) -> None:
    """ Сохраняет словарь с фильмами """
    user = User.get_or_none(User.user_id == user_id)
    
    if user:
        new_data = json.dumps(data)
        user.data = new_data
        user.save()
    else:
        print(f'{'-' * 10} Ошибка в функции db_set_films_data: пользователь с user_id {user_id} не найден')


def db_set_search_param(user_id: int, param: str, value: str) -> None:
    """ Сохраняет параметр поиска, для дальнейшего извлечения и запроса к серверу """
    user = User.get_or_none(User.user_id == user_id)
    
    if user:
        data = {param: value}
        old_param: dict = json.loads(user.search_param)
        old_param.update(data)
        user.search_param = json.dumps(old_param)
        user.save()
    else:
        print(f'{'-' * 10} Ошибка в функции db_set_search_param: пользователь с user_id {user_id} не найден')


def db_set_film_in_favorites(user_id: int, film_data: dict) -> None:
    """ Добавляет словарь с информацией о фильме в базу, раздел избранное """
    user: User = User.get_or_none(User.user_id == user_id)
    
    if user:
        cur_favourites: dict = json.loads(user.favourites)
        cur_favourites["favourites"].append(film_data)
        user.favourites = json.dumps(cur_favourites)
        user.save()
    else:
        print(f'{'-' * 10} Ошибка в функции db_set_film_in_favorites: пользователь с user_id {user_id} не найден')


def db_set_film_in_watched(user_id: int, film_id: int) -> None:
    """ Добавляет фильм в базу, словарь просмотренных """
    user: User = User.get_or_none(User.user_id == user_id)
    
    if user:
        cur_watched: dict = json.loads(user.watched_movies)
        cur_watched.update({film_id: True})
        user.watched_movies = json.dumps(cur_watched)
        user.save()
    else:
        print(f'{'-' * 10} Ошибка в функции db_set_film_in_watched: пользователь с user_id {user_id} не найден')


def db_set_action_history(user_id: int, text:str) -> None:
    """ Сохраняет историю поиска """
    user: User = User.get_or_none(User.user_id == user_id)
    
    if user:
        cur_history = json.loads(user.history)
        cur_history['history_search'].append(text)
        if len(cur_history['history_search']) > 20:
            cur_history['history_search'].pop(0)
        user.history = json.dumps(cur_history)
        user.save()
    else:
        print(f'{'-' * 10} Ошибка в функции db_set_action_history: пользователь с user_id {user_id} не найден')