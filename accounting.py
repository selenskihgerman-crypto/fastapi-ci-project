"""
Реализуйте приложение для учёта финансов, умеющее запоминать, сколько денег было потрачено за день,
а также показывать затраты за отдельный месяц и за целый год.

В программе должно быть три endpoints:

/add/<date>/<int:number> — сохранение информации о совершённой в рублях трате за какой-то день;
/calculate/<int:year> — получение суммарных трат за указанный год;
/calculate/<int:year>/<int:month> — получение суммарных трат за указанные год и месяц.

Дата для /add/ передаётся в формате YYYYMMDD, где YYYY — год, MM — месяц (от 1 до 12), DD — число (от 01 до 31).
Гарантируется, что переданная дата имеет такой формат и она корректна (никаких 31 февраля).
"""

import datetime
from flask import Flask

app = Flask(__name__)

storage = {}


@app.route("/add/<date>/<int:number>")
def add(date: str, number: int):
    try:
        expenses_date = datetime.datetime.strptime(date, '%Y%m%d')
        year, month, day = expenses_date.year, expenses_date.month, expenses_date.day
        storage.setdefault(year, {'total': 0}).setdefault(month, {'total': 0}).setdefault(day, 0)
        storage[year][month][day] += number
        storage[year]['total'] += number
        storage[year][month]['total'] += number

        print(storage)

        return f'Внесены расходы за {day}.{month}.{year} на сумму {number} рублей.'

    except ValueError as exc:
        print(f'ValueError: {exc}')
        return f'ValueError: {exc}'


@app.route("/calculate/<int:year>")
def calculate_year(year: int):
    try:
        return f'Расходы за {year} год: {storage[year]['total']} рублей.'
    except KeyError as exc:
        print(f'KeyError: {exc}')
        return 'Расходы за указанный период отсутствуют.'

@app.route("/calculate/<int:year>/<int:month>")
def calculate_month(year: int, month: int):
    try:
        return f'Расходы за {month}.{year} год: {storage[month][year]['total']} рублей.'
    except KeyError as exc:
        print(f'KeyError: {exc}')
        return 'Расходы за указанный период отсутствуют.'


if __name__ == "__main__":
    app.run(debug=True)
