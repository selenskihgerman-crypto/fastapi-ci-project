from flask import Flask
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/metrics')
def metrics_endpoint():
    return "# TYPE test_metric counter\ntest_metric 1\n", 200

# Добавляем новый эндпоинт с метрикой
@app.route('/custom')
@metrics.counter('custom_endpoint_requests', 'Number of requests to custom endpoint', labels={'status': lambda r: r.status_code})
def custom_endpoint():
    return "Custom endpoint response", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
