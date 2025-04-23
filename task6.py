from flask import Flask, redirect, url_for

app = Flask(__name__)

@app.errorhandler(404)
def page_not_found(e):
    available_pages = [str(rule) for rule in app.url_map.iter_rules()]
    return f"Страница не найдена. Доступные страницы: {', '.join(available_pages)}", 404

# Пример endpoint
@app.route('/')
def index():
    return "Главная страница"

if __name__ == '__main__':
    app.run()
