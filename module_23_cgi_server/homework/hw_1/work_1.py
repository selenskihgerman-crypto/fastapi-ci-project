import json
import time

class WSGIApp:
    def __init__(self):
        self.routes = {}
        
        @self.route("/hello")
        def hello():
            return json.dumps({"response": "Hello, world!"})
            
        @self.route("/hello/<name>")
        def hello_name(name):
            return json.dumps({"response": f"Hello, {name}!"})
            
        @self.route("/long_task")
        def long_task():
            time.sleep(300)
            return json.dumps({"message": "We did it!"})

    def route(self, path):
        def decorator(func):
            self.routes[path] = func
            return func
        return decorator

    def __call__(self, environ, start_response):
        path = environ.get('PATH_INFO', '')
        
        if path == '/hello':
            response = self.routes['/hello']()
        elif path.startswith('/hello/'):
            name = path.split('/')[-1]
            response = self.routes['/hello/<name>'](name)
        elif path == '/long_task':
            response = self.routes['/long_task']()
        else:
            start_response('404 Not Found', [('Content-Type', 'application/json')])
            return [json.dumps({"error": "Not Found"}).encode()]
            
        start_response('200 OK', [('Content-Type', 'application/json')])
        return [response.encode()]

app = WSGIApp()
