import json
import logging

class JsonAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        message = json.dumps({"time": self.formatTime(logging.LogRecord("", 0, "", 0, msg, [], None)), 
                               "level": logging.getLevelName(kwargs.get('level', logging.INFO)), 
                               "message": msg})
        return message, kwargs

logger = JsonAdapter(logging.getLogger(__name__))
logger.info('Sample log message')
