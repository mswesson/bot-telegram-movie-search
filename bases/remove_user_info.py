from bases.models import User
import json
from loader import bot


def db_remove_search_param(user_id: int) -> None:
    """ Убирает параметры поиска """
    user: User | None = User.get_or_none(User.user_id == user_id)
    
    if user:
        user.search_param = "{}"
        user.save()
    else:
        print(f'{'-' * 10} Ошибка в функции db_remove_search_param: пользователь с user_id {user_id} не найден')
        
        
def db_remove_film_in_favorites(user_id: int, film_id: int) -> None:
    """ Убирает фильм из избранных фильмов """
    user: User = User.get_or_none(User.user_id == user_id)
    
    if user:
        cur_favourites: dict = json.loads(user.favourites)
        for index, film in enumerate(cur_favourites["favourites"]):
            if film['id'] == film_id:
                cur_favourites["favourites"].pop(index)
                user.favourites = json.dumps(cur_favourites)
                user.save()
                return
        else:
            print(f'{'-' * 10} Ошибка в функции db_remove_film_in_favorites: фильм с film_id {film_id} не найден')
    else:
        print(f'{'-' * 10} Ошибка в функции db_remove_film_in_favorites: пользователь с user_id {user_id} не найден')


def db_remove_film_in_watched(user_id: int, film_id: int) -> None:
    """ Убирает фильм из просмотренных """
    user: User = User.get_or_none(User.user_id == user_id)
    
    if user:
        cur_watched: dict = json.loads(user.watched_movies)
        cur_watched.update({film_id: False})
        user.watched_movies = json.dumps(cur_watched)
        user.save()
    else:
        print(f'{'-' * 10} Ошибка в функции db_remove_film_in_watched: пользователь с user_id {user_id} не найден')