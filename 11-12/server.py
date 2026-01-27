import threading
import queue
import time
import random
import logging
from datetime import datetime

# Вспомогательная функция для отметки времени
def ts():
    return datetime.now().strftime("%H:%M:%S")

# Логирование
logging.basicConfig(
    filename="server.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)
logger = logging.getLogger("server_logger")

# ---------------------------------------------------------------------

# ТОЧНО ТАКИЕ ЖЕ АЛГОРИТМЫ, КАК В ВАШИХ ФАЙЛАХ

def execute_task_1_algorithm(arr1, arr2):
    """Алгоритм из task_1.py - задача 1"""
    # Сортируем: первый по убыванию, второй по возрастанию
    a = sorted(arr1, reverse=True)
    b = sorted(arr2)
    
    if len(a) != len(b):
        return [], [], []
    
    # Считаем с условием: если равны — 0
    result = []
    for i in range(len(a)):
        if a[i] == b[i]:
            result.append(0)
        else:
            result.append(a[i] + b[i])
    
    result = sorted(result)
    return result, a, b

def execute_task_4_algorithm(arr1, arr2, operation='+'):
    """Алгоритм из task_4.py - задача 4"""
    # Преобразуем массивы в числа
    num1 = int("".join(map(str, arr1)))
    num2 = int("".join(map(str, arr2)))
    
    if operation == '+':
        res = num1 + num2
    elif operation == '-':
        res = num1 - num2
    else:
        return ["Ошибка"]
    
    # Если отрицательное — добавляем минус
    if res < 0:
        return ['-', *list(map(int, str(-res)))]
    else:
        return list(map(int, str(res)))

def execute_task_5_algorithm(arr, target_sum):
    """Алгоритм из task_5.py - задача 5"""
    arr = list(map(int, arr)) 
    target = int(target_sum)
    count = 0
    n = len(arr)
    
    for i in range(n):
        sum_now = 0
        for j in range(i, n):
            sum_now += arr[j]
            if sum_now == target:
                count += 1
    return count

# ---------------------------------------------------------------------

class TaskServer(threading.Thread):
    """
    Сервер для задач 1, 4, 5.
    Клиенты подключаются и отправляют запросы через очередь.
    """

    def __init__(self, request_queue: queue.Queue, host='127.0.0.1', port=5000):
        super().__init__(daemon=True)
        self.request_queue = request_queue
        self.running = True
        self.processed = 0
        self.host = host
        self.port = port

    def run(self):
        logger.info("Сервер: инициализирован и готов к обработке запросов")
        logger.info("-" * 60)
        logger.info("СЕРВЕР ЗАДАЧ 1, 4, 5")
        logger.info("-" * 60)
        logger.info(f"Адрес: {self.host}:{self.port}")
        logger.info(f"Основной поток: ID {threading.get_ident()}")
        logger.info(f"Активные потоки: {threading.active_count()}\n")
        logger.info("Ожидание запросов от клиентов...\n")

        print(f"{ts()} Сервер: запущен")
        print(f"{ts()} Сервер: задачи 1, 4, 5")
        print(f"{ts()} Сервер: ожидание запросов...")
        print()

        # Основной цикл обработки запросов
        while self.running:
            try:
                # Получаем запрос из очереди
                request = self.request_queue.get(timeout=0.5)
            except queue.Empty:
                continue

            client = request.get('client')
            task = request.get('task')
            data = request.get('data')
            params = request.get('params', {})
            callback = request.get('callback')

            logger.info(f"{client}: получен запрос на {task}")
            print(f"{ts()} {client}: отправлен запрос на {self._task_name(task)}")

            # Эмуляция длительных расчетов
            delay = random.uniform(1, 3)
            logger.debug(f"Эмуляция расчета: задержка {delay:.2f} сек")
            time.sleep(delay)

            result = None
            try:
                if task == 'task1':
                    # Задача 1: обработка двух массивов
                    result_tuple = execute_task_1_algorithm(data['arr1'], data['arr2'])
                    result = {
                        'result': result_tuple[0],
                        'sorted_arr1': result_tuple[1],
                        'sorted_arr2': result_tuple[2],
                        'success': True
                    }
                    
                elif task == 'task4':
                    # Задача 4: арифметика чисел-массивов
                    operation = data.get('operation', '+')
                    result_list = execute_task_4_algorithm(data['arr1'], data['arr2'], operation)
                    result = {
                        'result': result_list,
                        'operation': operation,
                        'success': True
                    }
                    
                elif task == 'task5':
                    # Задача 5: подмассивы с заданной суммой
                    count = execute_task_5_algorithm(data['arr'], data['target'])
                    result = {
                        'result': count,
                        'success': True
                    }
                    
                else:
                    result = {
                        'success': False,
                        'error': f"Неизвестная задача: {task}"
                    }
                    
            except Exception as e:
                result = {
                    'success': False,
                    'error': str(e)
                }
                logger.exception(f"Ошибка при обработке запроса {task} от {client}")

            self.processed += 1
            logger.info(f"{client}: выполнена задача {task}")
            print(f"{ts()} {client}: выполнена {self._task_name(task)}")

            # Отправляем результат через callback
            if callable(callback):
                try:
                    callback(client, task, result, data)
                except Exception:
                    logger.exception(f"Ошибка в callback клиента {client}")

    def _task_name(self, task_key):
        """Возвращает читаемое имя задачи."""
        mapping = {
            'task1': 'обработку двух массивов',
            'task4': 'арифметику чисел-массивов',
            'task5': 'поиск подмассивов с заданной суммой'
        }
        return mapping.get(task_key, task_key)

    def stop(self):
        """Остановка сервера."""
        self.running = False
        logger.info(f"Сервер обработал {self.processed} запросов")
        print(f"\n{ts()} Сервер: обработано {self.processed} запросов")