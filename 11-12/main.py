#!/usr/bin/env python3
"""ЗАПУСК БОТА
Основной файл запуска, содержит только точку входа.
Файл должен находиться в корне проекта."""

import asyncio
from bot import run  # Импортируем основную функцию из bot.py

if __name__ == "__main__":
    # asyncio.run() запускает асинхронную функцию run()
    # Это стандартный способ запуска async/await кода в Python
    asyncio.run(run())
    # При нажатии Ctrl+C возникает KeyboardInterrupt, бот останавливается