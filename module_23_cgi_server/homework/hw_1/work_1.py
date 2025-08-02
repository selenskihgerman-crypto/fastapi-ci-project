# 1. wsgi_app.py (Задание 1 - WSGI-приложение)

import json
import time
from werkzeug.wrappers import Request, Response

class WSGIApp:
    def __init__(self):
        self.routes = {
            '/hello': self.handle_hello,
            '/hello/<name>': self.handle_hello_name,
            '/long_task': self.handle_long_task
        }

    def route(self, path):
        def decorator(func):
            self.routes[path] = func
            return func
        return decorator

    def handle_hello(self):
        return json.dumps({"response": "Hello, world!"})

    def handle_hello_name(self, name):
        return json.dumps({"response": f"Hello, {name}!"})

    def handle_long_task(self):
        time.sleep(300)  # 5-минутная задержка
        return json.dumps({"message": "We did it!"})

    def __call__(self, environ, start_response):
        request = Request(environ)
        path = request.path

        # Динамические маршруты
        if path.startswith('/hello/'):
            name = path.split('/')[-1]
            response = self.handle_hello_name(name)
            start_response('200 OK', [('Content-Type', 'application/json')])
            return [response.encode()]

        # Статические маршруты
        if path in self.routes:
            response = self.routes[path]()
            start_response('200 OK', [('Content-Type', 'application/json')])
            return [response.encode()]

        # 404
        start_response('404 Not Found', [('Content-Type', 'application/json')])
        return [json.dumps({"error": "Not Found"}).encode()]

app = WSGIApp()