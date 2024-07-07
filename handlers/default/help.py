from telebot.types import Message
from loader import bot
from bases.set_user_info import db_set_action_history
import datetime


@bot.message_handler(commands=['help'])
def help(message: Message) -> None:
    """ Сообщение при вызове команды /help """
    
    chat_id = message.chat.id
    user_id = message.from_user.id
    data_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    bot.send_message(
        chat_id=chat_id, 
        text=('Раздел помощь\n\n'
              'Список доступных команд:\n'
              '/help - Попасть в этот раздел.\n'
              '/start - Начинает всё сначала, регистрирует пользователя, база с избранными '
              'и просмотренными фильмами остается нетронутой.\n'
              '/favorites - Здесь хранятся все твои фильмы, которые ты ранее добавил, '
              'с помощью кнопки "Добавить в избранное" при поиске.\n'
              '/movie_search - Поиск фильма по названию. Тут всё просто, вводим название получаем '
              'самые близкие совпадения.\n'
              '/movie_by_budget - Поиск фильма по бюджету. Вводим диопазон бюждета, далее выбираем жанр '
              'и получаем результат.'))
    
    db_set_action_history(user_id=user_id, text=f'{data_now} - Заходим в раздел "Помощь"')
