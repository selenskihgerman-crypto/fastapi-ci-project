import logging

logging.basicConfig(
    filename="stderr.txt",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S"
)

logging.info("Hello, world!")  # Проверка: в stderr.txt появится строка с временем
