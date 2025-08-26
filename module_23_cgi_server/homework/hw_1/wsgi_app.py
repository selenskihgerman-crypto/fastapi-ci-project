# 1. WSGI-приложение (app/wsgi_app.py)
import json


class WSGIApp:
    def __call__(self, environ, start_response):
        path = environ.get('PATH_INFO', '/')

        if path == '/hello':
            status = '200 OK'
            response_data = {"response": "Hello, World!"}
        elif path.startswith('/hello/'):
            name = path.split('/')[-1]
            status = '200 OK'
            response_data = {"response": f"Hello, {name}!"}
        else:
            status = '404 Not Found'
            response_data = {"error": "Not Found"}

        response_body = json.dumps(response_data).encode('utf-8')
        headers = [
            ('Content-Type', 'application/json'),
            ('Content-Length', str(len(response_body)))
        ]
        start_response(status, headers)
        return [response_body]


app = WSGIApp()