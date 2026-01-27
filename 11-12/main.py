"""
Демонстрация клиент-серверного приложения для задач 1, 4, 5.
Сервер использует ТОЧНО ТАКИЕ ЖЕ алгоритмы, как в консольной версии.
"""

import queue
import time
import threading
from server import TaskServer
from client import ClientThread

def main():
    """
    Точка входа: создает очередь, запускает сервер и клиентов.
    """
    # Создаем очередь для обмена сообщениями
    q = queue.Queue()
    
    # Запускаем сервер
    server = TaskServer(q)
    server.start()
    
    # Даем серверу время на запуск
    time.sleep(0.5)
    
    # Создаем сценарии для клиентов (каждый клиент делает разные задачи)
    actions1 = [
        {'task': 'task1', 'generate': True, 'params': {'size': 5}},
        {'task': 'task4', 'generate': True, 'params': {'len_a': 3, 'len_b': 2}}
    ]
    
    actions2 = [
        {'task': 'task5', 'generate': True, 'params': {'size': 7}},
        {'task': 'task1', 'generate': True, 'params': {'size': 4}}
    ]
    
    actions3 = [
        {'task': 'task1', 'generate': True, 'params': {'size': 6}},
        {'task': 'task4', 'generate': True, 'params': {'len_a': 4, 'len_b': 3}},
        {'task': 'task5', 'generate': True, 'params': {'size': 8}}
    ]

    # Создаем и запускаем клиентов
    client1 = ClientThread("Клиент1", q, actions1)
    client2 = ClientThread("Клиент2", q, actions2)
    client3 = ClientThread("Клиент3", q, actions3)

    clients = [client1, client2, client3]
    
    print(f"\n{time.strftime('%H:%M:%S')} Запуск клиентов...")
    for c in clients:
        c.start()
        time.sleep(0.1)  # Небольшая задержка между запусками

    print(f"\nЗапущено клиентов: {len(clients)}")
    print(f"Всего активных потоков: {threading.active_count()}")
    print("=" * 60)
    print("Наблюдайте за параллельной работой клиентов!")
    print("=" * 60)
    print()

    # Ждем завершения всех клиентов
    for c in clients:
        c.join()

    # Даем серверу время обработать все оставшиеся задачи
    while not q.empty():
        time.sleep(0.2)

    # Подождем немного перед остановкой сервера
    time.sleep(1.0)

    # Останавливаем сервер
    server.stop()
    server.join(timeout=2.0)
    
    print("\n" + "=" * 60)
    print("ВСЕ ЗАДАЧИ ВЫПОЛНЕНЫ")
    print("=" * 60)
    print("Логи сервера сохранены в файле: server.log")

if __name__ == "__main__":
    main()