"""
Удобно сохранять логи в определённом формате, чтобы затем их можно было фильтровать и анализировать. 
Сконфигурируйте логгер так, чтобы он писал логи в файл skillbox_json_messages.log в следующем формате:

{"time": "<время>", "level": "<уровень лога>", "message": "<сообщение>"}

Но есть проблема: если в message передать двойную кавычку, то лог перестанет быть валидной JSON-строкой:

{"time": "21:54:15", "level": "INFO", "message": "“"}

Чтобы этого избежать, потребуется LoggerAdapter. Это класс из модуля logging,
который позволяет модифицировать логи перед тем, как они выводятся.
У него есть единственный метод — process, который изменяет сообщение или именованные аргументы, переданные на вход.

class JsonAdapter(logging.LoggerAdapter):
  def process(self, msg, kwargs):
    # меняем msg
    return msg, kwargs

Использовать можно так:

logger = JsonAdapter(logging.getLogger(__name__))
logger.info('Сообщение')

Вам нужно дописать метод process так, чтобы в логах была всегда JSON-валидная строка.
"""

import logging
import json
from datetime import datetime

class JsonAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        record = {
            "time": datetime.now().strftime("%H:%M:%S"),
            "level": kwargs.get("levelname", self.logger.level),
            "message": msg
        }
        kwargs["extra"] = {}
        return json.dumps(record, ensure_ascii=False), kwargs

logger = JsonAdapter(logging.getLogger(__name__), {})
handler = logging.FileHandler("skillbox_json_messages.log")
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
logger.logger.addHandler(handler)
logger.logger.setLevel(logging.INFO)

logger.info('Тестовое сообщение с кавычками " и переносом\nстроки')

