from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def keyboard_platform():
    """ Клавиатура для выбора платформы """
    
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = KeyboardButton(text='Кинопоиск')
    button2 = KeyboardButton(text='IMDb')
    button3 = KeyboardButton(text='Вернуться в главное меню')
    
    keyboard.add(button1, button2)
    keyboard.add(button3)
    
    return keyboard