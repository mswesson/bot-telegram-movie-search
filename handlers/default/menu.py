from telebot.types import Message
from loader import bot
from keyboards import key_menu
from bases.remove_user_info import db_remove_search_param
from handlers.special import movie_search, movie_by_budget, movie_by_rating, favorites_list, history
from handlers.default import help


MENU_COMMANDS = ['Поиск по названию', 'Поиск по рейтингу', 'Поиск по бюджету', 'Избранное', 'История', 'Помощь']


@bot.message_handler(func=lambda message: message.text == 'Вернуться в главное меню')
def go_back(message: Message) -> None:
    """ Возвращает в главное меню с любого режима при получении сообщения 'Вернуться в главное меню' """
    
    user_id = message.from_user.id
    chat_id = message.chat.id
    
    bot.send_message(chat_id=chat_id,
                     text='Вы вернулись в главное меню',
                     reply_markup=key_menu.key_menu())
    db_remove_search_param(user_id=user_id)
    bot.delete_state(user_id=user_id, chat_id=chat_id)
    
    
@bot.message_handler(func=lambda message: message.text in MENU_COMMANDS)
def menu(message: Message) -> None:
    """ Определяет какая команда была передана пользователем и запускает относительно неё режим """
    if message.text == 'Поиск по названию':
        movie_search.movie_search(message)
    elif message.text == 'Поиск по рейтингу':
        movie_by_rating.movie_by_rating(message)
    elif message.text == 'Поиск по бюджету':
        movie_by_budget.movie_by_budget(message)
    elif message.text == 'Избранное':
        favorites_list.favorites(message)
    elif message.text == 'История':
        history.history(message)
    elif message.text == 'Помощь':
        help.help(message)
