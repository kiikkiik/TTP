import threading
import time
import random
from datetime import datetime

def ts():
    return datetime.now().strftime("%H:%M:%S")

class ClientThread(threading.Thread):
    """
    Клиент с диалоговым меню для задач 1, 4, 5.
    Генерирует запросы и отправляет их в очередь сервера.
    """

    def __init__(self, name: str, request_queue, actions):
        super().__init__(daemon=True)
        self.name = name
        self.request_queue = request_queue
        self.actions = actions
        self.results = []

    def run(self):
        print(f"{ts()} {self.name}: клиент запущен")
        time.sleep(random.uniform(0.05, 0.25))

        # Проходим по всем действиям клиента
        for action in self.actions:
            task = action['task']  # 'task1', 'task4', 'task5'
            params = action.get('params', {})
            data = action.get('data')

            # Генерация данных для задач (как в консольной версии)
            if action.get('generate', False):
                if task == 'task1':
                    # Задача 1: два массива
                    size = random.randint(3, 8)
                    a = [random.randint(-10, 10) for _ in range(size)]
                    b = [random.randint(-10, 10) for _ in range(size)]
                    data = {'arr1': a, 'arr2': b}
                    print(f"{ts()} {self.name}: сгенерированы массивы для обработки")
                    print(f"  Первый массив: {a}")
                    print(f"  Второй массив: {b}")
                    print()
                    
                elif task == 'task4':
                    # Задача 4: числа-массивы
                    len_a = random.randint(2, 4)
                    len_b = random.randint(2, 4)
                    a = [random.randint(0, 9) for _ in range(len_a)]
                    b = [random.randint(0, 9) for _ in range(len_b)]
                    operation = random.choice(['+', '-'])
                    data = {'arr1': a, 'arr2': b, 'operation': operation}
                    print(f"{ts()} {self.name}: сгенерированы числа для арифметики")
                    print(f"  Первое число: {a}")
                    print(f"  Второе число: {b}")
                    print(f"  Операция: {operation}")
                    print()
                    
                elif task == 'task5':
                    # Задача 5: массив и сумма
                    size = random.randint(5, 10)
                    arr = [random.randint(-5, 5) for _ in range(size)]
                    target = random.randint(-10, 10)
                    data = {'arr': arr, 'target': target}
                    print(f"{ts()} {self.name}: сгенерированы данные для поиска подмассивов")
                    print(f"  Массив: {arr}")
                    print(f"  Целевая сумма: {target}")
                    print()

            # Отправка запроса на сервер
            task_name = self._task_name(task)
            print(f"{ts()} {self.name}: отправлен запрос на {task_name}")
            
            request = {
                'client': self.name,
                'task': task,
                'data': data,
                'params': params,
                'callback': self._callback
            }
            self.request_queue.put(request)

            # Пауза между запросами
            time.sleep(random.uniform(0.2, 0.9))

        print(f"{ts()} {self.name}: выполнение завершено")

    def _callback(self, client_name, task, result, input_data):
        """Callback функция, вызываемая сервером."""
        print(f"{ts()} {self.name}: получен результат для {self._task_name(task)}")
        
        if not result.get('success', False):
            print(f"  Ошибка: {result.get('error', 'Неизвестная ошибка')}")
            print()
        else:
            if task == 'task1':
                print("  Результаты задачи 1:")
                print(f"  Отсортированный первый массив (по убыванию): {result['sorted_arr1']}")
                print(f"  Отсортированный второй массив (по возрастанию): {result['sorted_arr2']}")
                print(f"  Итоговый массив: {result['result']}")
                print()
                
            elif task == 'task4':
                arr1 = input_data['arr1']
                arr2 = input_data['arr2']
                operation = input_data.get('operation', '+')
                result_list = result['result']
                
                # Форматируем вывод как в консольной версии
                if isinstance(result_list[0], str) and result_list[0] == '-':
                    formatted_result = "−" + "".join(map(str, result_list[1:]))
                else:
                    formatted_result = "".join(map(str, result_list))
                
                num1_str = ''.join(map(str, arr1))
                num2_str = ''.join(map(str, arr2))
                
                print("  Результаты задачи 4:")
                print(f"  Вычисление: {num1_str} {operation} {num2_str} = {formatted_result}")
                print(f"  Результат в виде массива: {result_list}")
                print()
                
            elif task == 'task5':
                print("  Результаты задачи 5:")
                print(f"  Массив: {input_data['arr']}")
                print(f"  Целевая сумма: {input_data['target']}")
                print(f"  Количество подмассивов: {result['result']}")
                print()
        
        # Сохраняем результат
        self.results.append((task, result))

    def _task_name(self, task_key):
        """Возвращает читаемое имя задачи."""
        mapping = {
            'task1': 'обработку двух массивов',
            'task4': 'арифметику чисел-массивов',
            'task5': 'поиск подмассивов с заданной суммой'
        }
        return mapping.get(task_key, task_key)