from bases.models import User
import json
from loader import bot
from typing import Optional


def db_checking_user(user_id: int) -> bool:
    """ Проверяет есть ли такой пользователь в базе данных """
    user: User = User.get_or_none(User.user_id == user_id)
    
    if user:
        return True
    else:
        return False


def db_checking_film_in_favourites(user_id: int, film_id: int) -> bool:
    """ Проверяет есть ли фильм в списке избранных фильмов """
    user: User = User.get_or_none(User.user_id == user_id)
    
    if user:
        cur_favourites: dict = json.loads(user.favourites)
        for film in cur_favourites["favourites"]:
            if film.get("id") == film_id:
                return True
        else:
            return False
    else:
        print(f'{'-' * 10} Ошибка в функции db_checking_film_in_favourites: пользователь с user_id {user_id} не найден')


def db_checking_film_in_watched(user_id: int, film_id: int) -> bool:
    """ Проверяет есть ли фильм в списке просмотренных """
    user: User = User.get_or_none(User.user_id == user_id)
    
    if user:
        dict_films_watched: dict = json.loads(user.watched_movies)
        film_watched: bool = dict_films_watched.get(str(film_id), False)
        return film_watched
    else:
        print(f'{'-' * 10} Ошибка в функции db_checking_film_in_watched: пользователь с user_id {user_id} не найден')
