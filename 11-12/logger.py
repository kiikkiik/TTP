"""
logger.py - модуль для логирования
"""

import logging

# Создаём конфигурацию логирования
logging.basicConfig(
    filename="app.log",                                 # файл для логирования
    level=logging.INFO,                                 # уровень логирования (фильтр сообщений)
    format="%(asctime)s - %(levelname)s - %(message)s", # формат записи логов
    encoding="utf-8"                                    # кодировка файла
)

# создание логгера с именем "app_logger"
logger = logging.getLogger("app_logger")