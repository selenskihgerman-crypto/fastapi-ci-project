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
