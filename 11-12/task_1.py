"""
Task 1 — обработка двух массивов (FSM-корутина)
"""

import random
import logging
from messages import MESSAGES

logger = logging.getLogger(__name__)
msgs = MESSAGES["task1"]


def execute_task_1_algorithm(arr1: list[int], arr2: list[int]) -> tuple:
    """Основной алгоритм задания 1."""
    if len(arr1) != len(arr2):
        error_msg = f"Массивы должны быть одинаковой длины. Длина первого: {len(arr1)}, второго: {len(arr2)}"
        raise ValueError(error_msg)
    
    if not arr1 or not arr2:
        raise ValueError("Массив не может быть пустым")
    
    try:
        # Сортируем: первый по убыванию, второй по возрастанию
        a = sorted(arr1, reverse=True)
        b = sorted(arr2)
        
        # Считаем с условием: если равны — 0
        result = []
        for i in range(len(a)):
            if a[i] == b[i]:
                result.append(0)
            else:
                sum_val = a[i] + b[i]
                if abs(sum_val) > 10**9:
                    logger.warning(f"Большая сумма: {sum_val}")
                result.append(sum_val)
        
        result = sorted(result)
        return result, a, b
        
    except Exception as e:
        raise RuntimeError(f"Ошибка вычислений: {e}")


def task1_fsm():
    """
    Корутина конечного автомата задачи 1.
    
    Состояния:
        NO_DATA   — массивы не заданы
        HAS_DATA  — массивы заданы
        HAS_RESULT — выполнен подсчёт
    """
    arr1 = None
    arr2 = None
    result = None
    sorted1 = None
    sorted2 = None
    state = "NO_DATA"

    while True:
        print("\n" + msgs["title"])
        for option in msgs["menu"]:
            print(option)

        choice = yield
        logger.info(f"task1 choice={choice}, state={state}")

        if choice == "5":
            return

        if state == "NO_DATA":
            if choice == "1":
                try:
                    arr1 = list(map(int, input("Первый массив: ").split()))
                    arr2 = list(map(int, input("Второй массив: ").split()))
                    state = "HAS_DATA"
                    logger.info("Arrays input manually")
                except Exception as e:
                    print(msgs["input_error"])
                    logger.error(f"Input error: {e}")
                    
            elif choice == "2":
                try:
                    size1 = int(input("Размер первого массива: "))
                    size2 = int(input("Размер второго массива: "))
                    arr1 = [random.randint(-10, 10) for _ in range(size1)]
                    arr2 = [random.randint(-10, 10) for _ in range(size2)]
                    print("Первый массив:", arr1)
                    print("Второй массив:", arr2)
                    state = "HAS_DATA"
                    logger.info("Arrays generated randomly")
                except Exception as e:
                    print(msgs["input_error"])
                    logger.error(f"Generation error: {e}")
            else:
                print(msgs["no_data"])

        elif state in ("HAS_DATA", "HAS_RESULT"):
            if choice == "3":
                try:
                    result, sorted1, sorted2 = execute_task_1_algorithm(arr1, arr2)
                    state = "HAS_RESULT"
                    print(msgs["calculation_done"])
                    logger.info("Algorithm executed")
                except Exception as e:
                    print(msgs["no_data"])
                    logger.error(f"Calculation error: {e}")
                    
            elif choice == "4":
                if result is None:
                    print(msgs["no_data"])
                else:
                    print("\nРезультаты:")
                    print(f"Отсортированный первый массив (по убыванию): {sorted1}")
                    print(f"Отсортированный второй массив (по возрастанию): {sorted2}")
                    print(f"Итоговый массив: {result}")
                    logger.info("Result displayed")
                    
            elif choice == "6":
                logger.setLevel("CRITICAL")
                print("Логирование отключено")
                logger.critical("Logging disabled")
            else:
                print(msgs["invalid_choice"])
                logger.info("Invalid menu choice")