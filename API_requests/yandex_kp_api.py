import json
import requests
from config_data.config import KINOPOISK_API
from copy import deepcopy
from typing import Optional
from bases.cheking_user_info import db_checking_film_in_watched
from bases.get_user_info import db_get_films_data


# Глобальные переменные
BASE_URL = "https://api.kinopoisk.dev/v1.4/movie"
HEADERS = {"accept": "application/json",
           "X-API-KEY": KINOPOISK_API,}
MOVIE_SEARCH_PARAMS = {"page": "1",
                       "limit": "1",
                       'selectFields': ['name', 'alternativeName', 'shortDescription', 'ageRating', 'id',
                                        'genres', 'countries', 'rating', 'poster', 'year', 'budget'],
                       'notNullFields': ['name', 'poster.url', 'shortDescription', 'ageRating', 'id',     
                                         'budget.value', 'budget.currency', 'year', 'countries.name']}


def yandex_requests(query: Optional[str] = None, 
                    platform: Optional[str] = None, 
                    rating: Optional[str] = None, 
                    genres: Optional[str] = None,
                    budget: Optional[str] = None,
                    page: int = 1,
                    limit: int = 30) -> Optional[dict]:
    
    """ 
    Запрос к серверу кинопоиска по введенным параметрам.
    Если было передано название, то остальные параметры не нужны.
    
    Аргументы:
        query (str): название фильма
        platform (str): платформа, например - кинопоиск
        rating (str): диапазон рейтинга
        genres (str): жанр
        budget (str): диапазон бюджета
        page (int): страница с результатом
        limit (int): лимит результатов на одной странице
        
    Вывод:
        (dict): словарь в формате JSON с результатами запроса
    """
    
    if query is not None:
        url = f'{BASE_URL}/search'
        
        params = deepcopy(MOVIE_SEARCH_PARAMS)
        params.update({"limit": "50", 
                       "query": query})
        params.pop('selectFields')
        params.pop('notNullFields')
        
        headers = HEADERS
    elif platform is not None and genres is not None:
        url = BASE_URL
        
        params = deepcopy(MOVIE_SEARCH_PARAMS)
        params.update({"limit": limit,
                       platform: rating,
                       "genres.name": genres})

        headers = HEADERS
    elif budget is not None and genres is not None:
        url = BASE_URL
        
        params = deepcopy(MOVIE_SEARCH_PARAMS)
        params.update({"limit": limit,
                       "budget.value": budget,
                       "genres.name": genres})

        headers = HEADERS
    
    response = requests.get(url=url, 
                            params=params, 
                            headers=headers)
    
    if response.ok:
        response_json = json.loads(response.text)
    else:
        print(f'{'-' * 10} Сервер кинопоиска вернул код {response.status_code}')
        return
    
    bad_films_index = list()  # Список с индексами фильмов, которые не удовлетворяют нашим потребностям
    for index, elem in enumerate(response_json["docs"]):  # Перебираем каждый фильм на полноту информации
        poster: str = elem["poster"]["previewUrl"]            
        year: int = elem["year"]
        age_rating: int = elem["ageRating"]
        short_description: str = elem["shortDescription"]

        if not poster or not year or not age_rating or not short_description:
            bad_films_index.append(index)

    for index in bad_films_index[::-1]:  # Удаляем фильмы, которые попали в список плохишей
        response_json["docs"].pop(index)
        
    response_json['total_2'] = len(response_json['docs'])
    
    return response_json


#######################################################################################


def see_result(data: dict,
               user_id: int, 
               number: int = 0,
               name_param: str = 'docs') -> Optional[tuple]:
    """
    Отправка результата поиска
    
    Аргументы:
        data (dict): словарь, где хранится информация о фильмах
        user_id (dict): id пользователя, обязательный параметр
        number (int): порядковый номер фильма
        name_param (str): если ключ словаря отличается от "docs"
    
    Вывод: 
        (tuple): выводит кортеж с двумя объектами: 
            - Первый содержит в себе url постера
            - Второй строку с названием, описание фильма и прочей информацией 
    """
    
    if db_get_films_data(user_id=user_id)["total"] == 0:  # проверяем найден ли хотябы один фильм
        print(f'Ошибка в функции see_result: пользователь с user_id {user_id} не найден')
        return
    
    simple_data: dict = data[name_param][number]
    poster_url: str = simple_data["poster"]["previewUrl"]
    name: str = simple_data["name"]
    english_name: str = simple_data["alternativeName"]
    year: int = simple_data["year"]
    age_rating: int = simple_data["ageRating"]
    watched_before: bool = db_checking_film_in_watched(user_id=user_id, film_id=simple_data["id"])
    genres: list = [genre["name"] for genre in simple_data["genres"]]
    countries: list = [country["name"] for country in simple_data["countries"]]
    budget: int | bool = False
    if simple_data.get("budget"):
        budget: int = simple_data["budget"]["value"]
        budget_currency: str = simple_data["budget"]["currency"]
    short_description: str = simple_data["shortDescription"]
    rating_kp: int = simple_data["rating"]["kp"]
    rating_imdb: int = simple_data["rating"]["imdb"]
    
    text = (f"{name} ({english_name}) | {year}  {age_rating}\n\n" if english_name else 
            f"{name} | {year}  {age_rating}\n\n")
    text += ("[ Вы посмотрели этот фильм ]\n\n" if watched_before else 
             "[ Вы не смотрели этот фильм ]\n\n")
    text += (f"- Жанр: {', '.join(genres)}\n"
             f"- Страна: {', '.join(countries)}\n")
    text += (f"- Бюджет: {budget:,.0f} {budget_currency}\n" if budget else "")
    text += (f"\n{short_description}.\n\n"
             f"Кинопоиск: {rating_kp}        IMBd: {rating_imdb}")
    
    return poster_url, text