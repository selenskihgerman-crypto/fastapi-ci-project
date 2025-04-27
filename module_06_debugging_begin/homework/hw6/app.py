"""
Заменим сообщение "The requested URL was not found on the server" на что-то более информативное.
Например, выведем список всех доступных страниц с возможностью перехода по ним.

Создайте Flask Error Handler, который при отсутствии запрашиваемой страницы будет выводить
список всех доступных страниц на сайте с возможностью перехода на них.
"""

from flask import Flask, render_template_string

app = Flask(__name__)

def get_routes():
    return [str(rule) for rule in app.url_map.iter_rules()
            if "GET" in rule.methods and not rule.arguments]

@app.errorhandler(404)
def page_not_found(e):
    links = "".join(f'<li><a href="{route}">{route}</a></li>' for route in get_routes())
    return f"<h1>Страница не найдена</h1><ul>{links}</ul>", 404

@app.route("/")
def index():
    return "Главная"

@app.route("/about")
def about():
    return "О сайте"

if __name__ == "__main__":
    app.run()

