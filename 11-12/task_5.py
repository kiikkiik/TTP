"""
Task 5 — подмассивы с заданной суммой (FSM-корутина)
"""

import logging
from messages import MESSAGES

logger = logging.getLogger(__name__)
msgs = MESSAGES["task5"]


def execute_task_5_algorithm(arr: list[int], target_sum: int) -> int:
    """Основной алгоритм задания 5."""
    try:
        count = 0
        n = len(arr)
        
        if n == 0:
            return 0
        
        for i in range(n):
            current_sum = 0
            for j in range(i, n):
                current_sum += arr[j]
                
                if abs(current_sum) > 10**9:
                    logger.warning(f"Большая промежуточная сумма: {current_sum}")
                
                if current_sum == target_sum:
                    count += 1
                    logger.debug(f"Найден подмассив с индексами [{i}:{j+1}]: {arr[i:j+1]}")
        
        return count
        
    except Exception as e:
        raise RuntimeError(f"Ошибка вычислений: {e}")


def task5_fsm():
    """
    Корутина конечного автомата задачи 5.
    
    Состояния:
        NO_DATA    — данные не введены
        HAS_ARRAY  — введен массив
        READY      — введена сумма
        HAS_RESULT — получен результат
    """
    arr = None
    target = None
    count = None
    state = "NO_DATA"

    while True:
        print("\n" + msgs["title"])
        for option in msgs["menu"]:
            print(option)

        choice = yield
        logger.info(f"task5 choice={choice}, state={state}")

        if choice == "5":
            return

        if state == "NO_DATA":
            if choice == "1":
                try:
                    arr = list(map(int, input("Введите массив чисел (через пробел): ").split()))
                    print(f"Массив установлен: {arr}")
                    state = "HAS_ARRAY"
                    logger.info("Array input")
                except Exception as e:
                    print(msgs["input_error"])
                    logger.error(f"Input error: {e}")
            else:
                print(msgs["no_data"])

        elif state == "HAS_ARRAY":
            if choice == "1":
                try:
                    arr = list(map(int, input("Введите массив чисел (через пробел): ").split()))
                    print(f"Массив обновлен: {arr}")
                    count = None
                    logger.info("Array updated")
                except Exception as e:
                    print(msgs["input_error"])
                    logger.error(f"Input error: {e}")
            elif choice == "2":
                try:
                    target = int(input("Целевая сумма: ").strip())
                    print(f"Целевая сумма установлена: {target}")
                    state = "READY"
                    logger.info("Target sum input")
                except Exception as e:
                    print(msgs["input_error"])
                    logger.error(f"Input error: {e}")
            else:
                print(msgs["no_data"])

        elif state in ("READY", "HAS_RESULT"):
            if choice == "1":
                try:
                    arr = list(map(int, input("Введите массив чисел (через пробел): ").split()))
                    print(f"Массив обновлен: {arr}")
                    count = None
                    state = "HAS_ARRAY"
                    logger.info("Array updated")
                except Exception as e:
                    print(msgs["input_error"])
                    logger.error(f"Input error: {e}")
            elif choice == "2":
                try:
                    target = int(input("Целевая сумма: ").strip())
                    print(f"Целевая сумма обновлена: {target}")
                    state = "READY"
                    logger.info("Target sum updated")
                except Exception as e:
                    print(msgs["input_error"])
                    logger.error(f"Input error: {e}")
            elif choice == "3":
                try:
                    count = execute_task_5_algorithm(arr, target)
                    state = "HAS_RESULT"
                    print(msgs["calculation_done"])
                    logger.info(f"Subarrays found: {count}")
                except Exception as e:
                    print(msgs["no_data"])
                    logger.error(f"Calculation error: {e}")
            elif choice == "4":
                if count is None:
                    print(msgs["no_data"])
                else:
                    print(f"Массив: {arr}")
                    print(f"Целевая сумма: {target}")
                    print(f"Количество подмассивов с суммой {target}: {count}")
                    logger.info("Result displayed")
            elif choice == "6":
                logger.setLevel("CRITICAL")
                print("Логирование отключено")
                logger.critical("Logging disabled")
            else:
                print(msgs["invalid_choice"])
                logger.info("Invalid menu choice")