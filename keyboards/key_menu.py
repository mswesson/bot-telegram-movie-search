from telebot.types import ReplyKeyboardMarkup, KeyboardButton

def key_back():
    """ Клавиатура для возврата в главное меню """
    
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    button = KeyboardButton(text='Вернуться в главное меню')
    
    keyboard.add(button)
    
    return keyboard


def key_menu():
    """ Клавиатура главное меню """
    
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = KeyboardButton(text='Поиск по названию')
    button2 = KeyboardButton(text='Поиск по рейтингу')
    button3 = KeyboardButton(text='Поиск по бюджету')
    button4 = KeyboardButton(text='Избранное')
    button5 = KeyboardButton(text='История')
    button6 = KeyboardButton(text='Помощь')
    
    keyboard.add(button1, button2, button3)
    keyboard.add(button4, button5, button6)
    
    return keyboard
    