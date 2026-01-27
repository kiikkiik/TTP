"""
Task 4 — арифметика чисел-массивов (FSM-корутина)
"""

import logging
from messages import MESSAGES

logger = logging.getLogger(__name__)
msgs = MESSAGES["task4"]


def execute_task_4_algorithm(arr1: list[int], arr2: list[int], operation: str) -> list:
    """Основной алгоритм задания 4."""
    try:
        # Преобразуем массивы в числа
        num1 = int(''.join(map(str, arr1)))
        num2 = int(''.join(map(str, arr2)))
        
        # Выполняем операцию
        if operation == '+':
            result = num1 + num2
        else:  # operation == '-'
            result = num1 - num2
            if result < 0:
                raise ValueError(f"Результат отрицательный: {result}")
        
        # Преобразуем результат обратно в массив цифр
        if result < 0:
            result_digits = ['-'] + [int(d) for d in str(abs(result))]
        else:
            result_digits = [int(d) for d in str(result)]
        
        return result_digits
        
    except OverflowError:
        raise RuntimeError("Переполнение при вычислениях")
    except Exception as e:
        raise RuntimeError(f"Ошибка вычислений: {e}")


def task4_fsm():
    """
    Корутина конечного автомата задачи 4.
    
    Состояния:
        NO_DATA    — данные не введены
        HAS_FIRST  — введено первое число
        HAS_BOTH   — введены оба числа
        READY      — введена операция
        HAS_RESULT — получен результат
    """
    arr1 = None
    arr2 = None
    operation = None
    result = None
    state = "NO_DATA"

    while True:
        print("\n" + msgs["title"])
        for option in msgs["menu"]:
            print(option)

        choice = yield
        logger.info(f"task4 choice={choice}, state={state}")

        if choice == "6":
            return

        if state == "NO_DATA":
            if choice == "1":
                try:
                    arr1 = list(map(int, input("Введите первое число (цифры через пробел): ").split()))
                    for digit in arr1:
                        if not (0 <= digit <= 9):
                            raise ValueError("Все цифры должны быть от 0 до 9")
                    print(f"Первое число установлено: {arr1}")
                    state = "HAS_FIRST"
                    logger.info("First number input")
                except Exception as e:
                    print(msgs["input_error"])
                    logger.error(f"Input error: {e}")
            else:
                print(msgs["no_data"])

        elif state == "HAS_FIRST":
            if choice == "1":
                try:
                    arr1 = list(map(int, input("Введите первое число (цифры через пробел): ").split()))
                    for digit in arr1:
                        if not (0 <= digit <= 9):
                            raise ValueError("Все цифры должны быть от 0 до 9")
                    print(f"Первое число установлено: {arr1}")
                    logger.info("First number updated")
                except Exception as e:
                    print(msgs["input_error"])
                    logger.error(f"Input error: {e}")
            elif choice == "2":
                try:
                    arr2 = list(map(int, input("Введите второе число (цифры через пробел): ").split()))
                    for digit in arr2:
                        if not (0 <= digit <= 9):
                            raise ValueError("Все цифры должны быть от 0 до 9")
                    print(f"Второе число установлено: {arr2}")
                    state = "HAS_BOTH"
                    logger.info("Second number input")
                except Exception as e:
                    print(msgs["input_error"])
                    logger.error(f"Input error: {e}")
            else:
                print(msgs["no_data"])

        elif state == "HAS_BOTH":
            if choice == "1":
                try:
                    arr1 = list(map(int, input("Введите первое число (цифры через пробел): ").split()))
                    for digit in arr1:
                        if not (0 <= digit <= 9):
                            raise ValueError("Все цифры должны быть от 0 до 9")
                    print(f"Первое число обновлено: {arr1}")
                    logger.info("First number updated")
                except Exception as e:
                    print(msgs["input_error"])
                    logger.error(f"Input error: {e}")
            elif choice == "2":
                try:
                    arr2 = list(map(int, input("Введите второе число (цифры через пробел): ").split()))
                    for digit in arr2:
                        if not (0 <= digit <= 9):
                            raise ValueError("Все цифры должны быть от 0 до 9")
                    print(f"Второе число обновлено: {arr2}")
                    logger.info("Second number updated")
                except Exception as e:
                    print(msgs["input_error"])
                    logger.error(f"Input error: {e}")
            elif choice == "3":
                try:
                    operation = input("Операция (+ или -): ").strip()
                    if operation not in ['+', '-']:
                        raise ValueError("Операция должна быть '+' или '-'")
                    print(f"Операция установлена: {operation}")
                    state = "READY"
                    logger.info("Operation input")
                except Exception as e:
                    print(msgs["input_error"])
                    logger.error(f"Input error: {e}")
            else:
                print(msgs["no_data"])

        elif state in ("READY", "HAS_RESULT"):
            if choice == "1":
                try:
                    arr1 = list(map(int, input("Введите первое число (цифры через пробел): ").split()))
                    for digit in arr1:
                        if not (0 <= digit <= 9):
                            raise ValueError("Все цифры должны быть от 0 до 9")
                    print(f"Первое число обновлено: {arr1}")
                    state = "HAS_FIRST"
                    logger.info("First number updated")
                except Exception as e:
                    print(msgs["input_error"])
                    logger.error(f"Input error: {e}")
            elif choice == "2":
                try:
                    arr2 = list(map(int, input("Введите второе число (цифры через пробел): ").split()))
                    for digit in arr2:
                        if not (0 <= digit <= 9):
                            raise ValueError("Все цифры должны быть от 0 до 9")
                    print(f"Второе число обновлено: {arr2}")
                    state = "HAS_BOTH"
                    logger.info("Second number updated")
                except Exception as e:
                    print(msgs["input_error"])
                    logger.error(f"Input error: {e}")
            elif choice == "3":
                try:
                    operation = input("Операция (+ или -): ").strip()
                    if operation not in ['+', '-']:
                        raise ValueError("Операция должна быть '+' или '-'")
                    print(f"Операция установлена: {operation}")
                    state = "READY"
                    logger.info("Operation updated")
                except Exception as e:
                    print(msgs["input_error"])
                    logger.error(f"Input error: {e}")
            elif choice == "4":
                try:
                    result = execute_task_4_algorithm(arr1, arr2, operation)
                    state = "HAS_RESULT"
                    print(msgs["calculation_done"])
                    logger.info("Calculation executed")
                except Exception as e:
                    print(msgs["no_data"])
                    logger.error(f"Calculation error: {e}")
            elif choice == "5":
                if result is None:
                    print(msgs["no_data"])
                else:
                    if isinstance(result[0], str) and result[0] == '-':
                        formatted_result = "−" + "".join(map(str, result[1:]))
                    else:
                        formatted_result = "".join(map(str, result))
                    print(f"Результат: {formatted_result}")
                    logger.info("Result displayed")
            elif choice == "7":
                logger.setLevel("CRITICAL")
                print("Логирование отключено")
                logger.critical("Logging disabled")
            else:
                print(msgs["invalid_choice"])
                logger.info("Invalid menu choice")