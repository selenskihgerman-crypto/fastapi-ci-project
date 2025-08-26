from flask import Flask, request
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)

# Стандартные метрики
metrics.info('app_info', 'Application info', version='1.0.3')

@app.route('/')
def main():
    return "Hello World!"

@app.route('/metrics')
@metrics.counter('invocation_by_route', 'Number of invocations by route',
                 labels={'path': lambda: request.path, 'status': lambda r: r.status_code})
def metrics_endpoint():
    return "Metrics endpoint"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
