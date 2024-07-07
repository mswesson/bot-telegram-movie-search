from telebot.handler_backends import State, StatesGroup


class MovieSearch(StatesGroup):
    search = State()
    search_result = State()