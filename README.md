# Телеграмм бот для поиска фильмов
### Описание
Данный бот создан как дипломный проект Skillbox к модулю "python basic 2".

Бот может:
- Искать фильмы по названию
- Искать фильмы по рейтингу и жанру
- Искать фильмы по бюджету и жанру
- Сохранять фильмы в список избранного
- Показывать историю взаимодействия

### Установка
1. Клонируйте репозиторий к себе на компьютер с помощью IDE либо же командой в Git bash: `$ git clone https://gitlab.skillbox.ru/eduard_komarov/python_basic_diploma.git` прежде перейдя в директорию, куда вы хотите сохранить проект.
2. Создайте виртуальное окружение:
    1. Откройте терминал, сразу в дириктории с проектом, или перейдите туда командой `cd <путь к проекту>`
    2. Введите команду `python -m venv .venv`.
    3. Запустите файл через терминал командой `venv\Scripts\activate`.
    4. После активации ваш терминал должен показывать имя виртуального окружения, например: `(venv) /path/to/your/project`.
2. Установите библиотеки, которые находятся в файле "requirements.txt" с помошью команды в командной строке: `pip install -r requirements.txt`. Важно находиться в виртуальной среде при инсталяции библиотек.
3. Создайте токен Telegram через бота @BotFather и загрузите его в файл ".env.example" в переменную "TELEGRAM_TOKEN".
4. Создайте токен в сервсе Кинопоиска по [ссылке](https://kinopoisk.dev/), для этого необходимо будет зарегестрироваться. Загрузите данный токен в файл ".env.example" в переменную "KINOPOISK_API".
5. Переминуйте файл ".env.example" в ".env" и сохраните.

### Запуск
1. Запускайте файл "main.py".
2. Перейдите в Telegram и напишите команду `/start`.
3. Если все было выполнено правильно, бот должен работать.
