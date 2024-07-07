from telebot.types import ReplyKeyboardMarkup, KeyboardButton


GENRES_LIST = ['аниме', 'биография', 'боевик', "вестерн", "военный", 
               "детектив", "детский", "для взрослых", "документальный", 
               "драма", "игра", "история", "комедия", "концерт", 
               "короткометражка", "криминал", "мелодрама", "музыка", 
               "мультфильм", "мюзикл", "новости", "приключения", "реальное ТВ", 
               "семейный", "спорт", "ток-шоу", "триллер", "ужасы", "фантастика", 
               "фильм-нуар", "фэнтези", "церемония"]
   

def keyboard_genres() -> None:
    """ Клавиатура для выбора жанра """
    
    buttons_genres_list = list()
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    button_back = KeyboardButton(text='Вернуться в главное меню')
    
    for button_text in GENRES_LIST:
        buttons_genres_list.append(KeyboardButton(text=button_text))
    
    keyboard.add(*buttons_genres_list)
    keyboard.add(button_back)
    
    return keyboard
