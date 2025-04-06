import datetime
import random
from flask import Flask

app = Flask(__name__)


@app.route('/hello_world')
def test_function():
    return '<h1>Привет, мир!</h1>'


@app.route('/cars')
def test_function():
    # Список машин
    cars = ["Chevrolet", "Renault", "Ford", "Lada"]
    # Возврат списка машин через запятую
    return ", ".join(cars)


@app.route('/cats')
def random_cat():
    # Список пород кошек
    cat_breeds = [
        "корниш-рекс",
        "русская голубая",
        "шотландская вислоухая",
        "мейн-кун",
        "манчкин"
    ]
    # Выбираем случайную породу
    random_breed = random.choice(cat_breeds)
    # Возвращаем случайную породу
    return random_breed


@app.route('/get_time/now')
def get_time():
    # Получаем текущее время
    current_time = datetime.now().strftime("%H:%M:%S")
    # Возвращаем строку с текущим временем
    return f"Точное время: {current_time}"


@app.route('/get_time/future')
def get_time_future():
    # Получаем текущее время
    current_time = datetime.now()
    # Вычисляем время через 1 час
    time_after_hour = current_time + timedelta(hours=1)
    # Форматируем время в строку "HH:MM:SS"
    current_time_after_hour = time_after_hour.strftime("%H:%M:%S")
    # Возвращаем строку с временем через час
    return f"Точное время через час будет {current_time_after_hour}"


@app.route('/get_random_word')
def get_random_word():
    # Читаем содержимое файла с книгой
    try:
        with open("war_and_peace.txt", "r", encoding="utf-8") as file:
            # Считываем текст и разбиваем на слова
            text = file.read()
            words = text.split()
    except FileNotFoundError:
        return "Файл war_and_peace.txt не найден."

    # Выбираем случайное слово
    if words:
        random_word = random.choice(words)
        return f"Случайное слово из книги: {random_word}"
    else:
        return "Файл пуст или не содержит слов."


@app.route('/counter')
def count_visits():
    global counter  # Делаем переменную глобальной для изменения её значения
    counter += 1  # Увеличиваем счётчик при каждом посещении страницы
    return f"Страница была открыта {counter} раз(а)."


if __name__ == '__main__':
    app.run(debug=True)
