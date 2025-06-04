# Задача 8. Сборщик логов (Flask + HTTPHandler)

from flask import Flask, request, jsonify

app = Flask(__name__)
logs = []

@app.route('/log', methods=['POST'])
def log():
    logs.append(dict(request.form))
    return 'OK', 200

@app.route('/logs', methods=['GET'])
def get_logs():
    return jsonify(logs)

if __name__ == '__main__':
    app.run(port=3000)
