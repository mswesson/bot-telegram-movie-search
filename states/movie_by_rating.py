from telebot.handler_backends import State, StatesGroup


class MovieRating(StatesGroup):
    search_platform = State()
    search_rating = State()
    search_genres = State()