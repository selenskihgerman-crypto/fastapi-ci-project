# Реализация калькулятора

from flask import Flask
from flask_jsonrpc import JSONRPC

app = Flask(__name__)
jsonrpc = JSONRPC(app, '/api/jsonrpc')


@jsonrpc.method('Calculator.calculate')
def calculate(operation: str, a: float, b: float) -> dict:
    """Выполняет арифметические операции над двумя числами.

    Args:
        operation (str): Операция (add, subtract, multiply, divide)
        a (float): Первое число
        b (float): Второе число

    Returns:
        dict: Результат операции или сообщение об ошибке

    Raises:
        ValueError: При неверной операции или делении на ноль
    """
    try:
        if operation == 'add':
            result = a + b
        elif operation == 'subtract':
            result = a - b
        elif operation == 'multiply':
            result = a * b
        elif operation == 'divide':
            if b == 0:
                raise ValueError("Division by zero is not allowed")
            result = a / b
        else:
            raise ValueError("Invalid operation")

        return {
            'result': result,
            'operation': operation,
            'numbers': [a, b]
        }
    except Exception as e:
        return {
            'error': str(e),
            'code': -32602,
            'message': 'Invalid parameters'
        }, 400


# Документация для Swagger
calculate.api_doc = {
    "description": "Выполняет арифметические операции над двумя числами",
    "params": {
        "operation": {
            "type": "string",
            "enum": ["add", "subtract", "multiply", "divide"],
            "description": "Арифметическая операция"
        },
        "a": {
            "type": "number",
            "description": "Первое число"
        },
        "b": {
            "type": "number",
            "description": "Второе число"
        }
    },
    "returns": {
        "description": "Результат операции",
        "schema": {
            "type": "object",
            "properties": {
                "result": {
                    "type": "number",
                    "description": "Результат вычисления"
                },
                "operation": {
                    "type": "string",
                    "description": "Выполненная операция"
                },
                "numbers": {
                    "type": "array",
                    "items": {"type": "number"},
                    "description": "Исходные числа"
                }
            }
        }
    },
    "errors": [
        {
            "code": -32602,
            "message": "Invalid parameters",
            "description": "Возникает при неверной операции или делении на ноль"
        }
    ]
}

if __name__ == '__main__':
    app.run(debug=True)