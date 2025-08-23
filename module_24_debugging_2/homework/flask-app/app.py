from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/metrics')
def metrics():
    return "# TYPE test_metric counter\ntest_metric 1\n", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)