import json
import re

class WSGIApplication:
    def __init__(self):
        self.routes = {}
        self.error_handlers = {}

    def route(self, path):
        def decorator(func):
            # Преобразуем пути с параметрами в регулярные выражения
            pattern = re.sub(r'<(\w+)>', r'(?P<\1>[^/]+)', path)
            self.routes[(pattern, func.__name__)] = func
            return func
        return decorator

    def __call__(self, environ, start_response):
        path = environ.get('PATH_INFO', '/')
        method = environ.get('REQUEST_METHOD', 'GET')

        # Ищем подходящий маршрут
        for route_pattern, handler in self.routes.items():
            pattern, _ = route_pattern
            match = re.fullmatch(pattern, path)
            if match:
                # Вызываем обработчик с параметрами из URL
                response = handler(**match.groupdict())
                status = '200 OK'
                headers = [('Content-Type', 'application/json')]
                start_response(status, headers)
                return [response.encode('utf-8')]

        # Если маршрут не найден - 404
        status = '404 Not Found'
        headers = [('Content-Type', 'application/json')]
        start_response(status, headers)
        return [json.dumps({"error": "Not Found"}).encode('utf-8')]

app = WSGIApplication()

@app.route("/hello")
def say_hello():
    return json.dumps({"response": "Hello, world!"}, indent=4)

@app.route("/hello/<name>")
def say_hello_with_name(name: str):
    return json.dumps({"response": f"Hello, {name}!"}, indent=4)
