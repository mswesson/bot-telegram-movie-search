from telebot.handler_backends import State, StatesGroup


class MovieSearch(StatesGroup):
    search_budget = State()
    search_budget_genres = State()
    search_result_budget = State()