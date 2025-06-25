# Пример запроса к JSON-RPC калькулятору

import requests

url = "http://localhost:5000/api/jsonrpc"
headers = {'content-type': 'application/json'}

# Пример корректного запроса
payload = {
    "jsonrpc": "2.0",
    "method": "Calculator.calculate",
    "params": {
        "operation": "add",
        "a": 5,
        "b": 3
    },
    "id": 1
}

response = requests.post(url, json=payload, headers=headers).json()
print(response)  # {'result': 8, 'operation': 'add', 'numbers': [5, 3]}

# Пример запроса с ошибкой
payload_error = {
    "jsonrpc": "2.0",
    "method": "Calculator.calculate",
    "params": {
        "operation": "divide",
        "a": 5,
        "b": 0
    },
    "id": 2
}

response_error = requests.post(url, json=payload_error, headers=headers).json()
print(response_error)  # {'error': 'Division by zero is not allowed', 'code': -32602, 'message': 'Invalid parameters'}