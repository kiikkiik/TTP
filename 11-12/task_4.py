"""
Task 4 — арифметика чисел-массивов (FSM-меню)
"""

import logging
from exceptions import (
    CalculationError, InvalidArrayError, EmptyArrayError, InvalidNumberError,
    UnsupportedOperationError, NegativeResultError, ValidationError
)
from messages import MESSAGES

logger = logging.getLogger(__name__)
msgs = MESSAGES["task4"]

# Вспомогательные функции

def input_digits_array() -> list[int]:
    """Ввод массива цифр."""
    raw = input("Введите цифры через пробел (0-9): ")
    if not raw.strip():
        raise EmptyArrayError("Ввод не может быть пустым")
    
    try:
        digits = list(map(int, raw.split()))
        for digit in digits:
            if not (0 <= digit <= 9):
                raise InvalidNumberError("Все цифры должны быть от 0 до 9")
        return digits
    except ValueError:
        raise InvalidArrayError("Некорректные цифры")


def input_operation() -> str:
    """Ввод операции."""
    op = input("Операция (+ или -): ").strip()
    if op not in ['+', '-']:
        raise UnsupportedOperationError("Операция должна быть '+' или '-'")
    return op


def digits_to_number(digits: list[int]) -> int:
    """Преобразует массив цифр в число."""
    if not digits:
        return 0
    return int(''.join(map(str, digits)))


def number_to_digits(number: int) -> list:
    """Преобразует число в массив цифр."""
    if number == 0:
        return [0]
    
    if number < 0:
        return ['-'] + [int(d) for d in str(abs(number))]
    
    return [int(d) for d in str(number)]


def execute_task_4_algorithm(arr1: list[int], arr2: list[int], operation: str) -> list:
    """Основной алгоритм задания 4."""
    try:
        num1 = digits_to_number(arr1)
        num2 = digits_to_number(arr2)
        
        if operation == '+':
            result = num1 + num2
        else:  # operation == '-'
            result = num1 - num2
            if result < 0:
                raise NegativeResultError(f"Результат отрицательный: {result}")
        
        if result < 0:
            result_digits = ['-'] + [int(d) for d in str(abs(result))]
        else:
            result_digits = number_to_digits(result)
        
        return result_digits
        
    except OverflowError:
        raise CalculationError("Переполнение при вычислениях")
    except Exception as e:
        raise CalculationError(f"Ошибка вычислений: {e}")


# ОБРАБОТЧИКИ ДЕЙСТВИЙ FSM

def _input_first_number(state_container):
    """Ввод первого числа."""
    try:
        arr1 = input_digits_array()
        state_container["arr1"] = arr1
        print(f"Первое число установлено: {arr1}")
        logger.info("task4: первое число введено")
    except Exception as e:
        logger.error(str(e))
        print(msgs["input_error"])


def _input_second_number(state_container):
    """Ввод второго числа."""
    try:
        arr2 = input_digits_array()
        state_container["arr2"] = arr2
        print(f"Второе число установлено: {arr2}")
        logger.info("task4: второе число введено")
    except Exception as e:
        logger.error(str(e))
        print(msgs["input_error"])


def _input_operation(state_container):
    """Ввод операции."""
    try:
        operation = input_operation()
        state_container["operation"] = operation
        print(f"Операция установлена: {operation}")
        logger.info("task4: операция введена")
    except Exception as e:
        logger.error(str(e))
        print(msgs["input_error"])


def _perform_calculation(state_container):
    """Выполняет вычисление."""
    arr1 = state_container.get("arr1")
    arr2 = state_container.get("arr2")
    operation = state_container.get("operation")

    if arr1 is None or arr2 is None or operation is None:
        print(msgs["no_data"])
        logger.warning("task4: попытка вычисления без данных")
        return

    try:
        result = execute_task_4_algorithm(arr1, arr2, operation)
        state_container["result"] = result
        print(msgs["calculation_done"])
        logger.info("task4: вычисление выполнено")
    except Exception as e:
        logger.error(str(e))
        print(msgs["no_data"])


def _show_result(state_container):
    """Показывает результат."""
    result = state_container.get("result")
    arr1 = state_container.get("arr1")
    arr2 = state_container.get("arr2")
    operation = state_container.get("operation")

    if result is None:
        print(msgs["no_data"])
        logger.warning("task4: попытка показать результат без вычислений")
    else:
        print(f"\nПервое число: {arr1}")
        print(f"Второе число: {arr2}")
        print(f"Операция: {operation}")
        
        if isinstance(result[0], str) and result[0] == '-':
            formatted_result = "−" + "".join(map(str, result[1:]))
        else:
            formatted_result = "".join(map(str, result))
        
        print(f"Результат: {formatted_result}")
        logger.info("task4: результат показан")


def _disable_logging(state_container):
    """Отключает логирование."""
    logger.setLevel("CRITICAL")
    print("Логирование отключено")
    logger.critical("task4: логирование отключено")


def _back(state_container):
    """Возвращает в главное меню."""
    logger.info("task4: возврат в главное меню")


# ACTION MAP

ACTION_MAP = {
    "input_first": _input_first_number,
    "input_second": _input_second_number,
    "input_operation": _input_operation,
    "perform_calculation": _perform_calculation,
    "show_result": _show_result,
    "disable_logging": _disable_logging,
    "back": _back
}

# FSM TRANSITIONS

TRANSITIONS = {
    "NO_DATA": {
        "1": {"action": "input_first", "next": "HAS_FIRST"},
        "2": {"error": "no_first"},
        "3": {"error": "no_data"},
        "4": {"error": "no_data"},
        "5": {"error": "no_result"},
        "6": {"action": "back", "next": "BACK"},
        "7": {"action": "disable_logging", "next": "NO_DATA"},
    },
    "HAS_FIRST": {
        "1": {"action": "input_first", "next": "HAS_FIRST"},
        "2": {"action": "input_second", "next": "HAS_BOTH"},
        "3": {"error": "no_second"},
        "4": {"error": "no_data"},
        "5": {"error": "no_result"},
        "6": {"action": "back", "next": "BACK"},
        "7": {"action": "disable_logging", "next": "HAS_FIRST"},
    },
    "HAS_BOTH": {
        "1": {"action": "input_first", "next": "HAS_FIRST"},
        "2": {"action": "input_second", "next": "HAS_BOTH"},
        "3": {"action": "input_operation", "next": "READY"},
        "4": {"error": "no_operation"},
        "5": {"error": "no_result"},
        "6": {"action": "back", "next": "BACK"},
        "7": {"action": "disable_logging", "next": "HAS_BOTH"},
    },
    "READY": {
        "1": {"action": "input_first", "next": "HAS_FIRST"},
        "2": {"action": "input_second", "next": "HAS_BOTH"},
        "3": {"action": "input_operation", "next": "READY"},
        "4": {"action": "perform_calculation", "next": "HAS_RESULT"},
        "5": {"error": "no_result"},
        "6": {"action": "back", "next": "BACK"},
        "7": {"action": "disable_logging", "next": "READY"},
    },
    "HAS_RESULT": {
        "1": {"action": "input_first", "next": "HAS_FIRST"},
        "2": {"action": "input_second", "next": "HAS_BOTH"},
        "3": {"action": "input_operation", "next": "READY"},
        "4": {"action": "perform_calculation", "next": "HAS_RESULT"},
        "5": {"action": "show_result", "next": "HAS_RESULT"},
        "6": {"action": "back", "next": "BACK"},
        "7": {"action": "disable_logging", "next": "HAS_RESULT"},
    }
}

# ГЛАВНАЯ ФУНКЦИЯ МЕНЮ

def task4_menu():
    """Запускает FSM-меню задачи 4."""
    state_container = {
        "arr1": None,
        "arr2": None,
        "operation": None,
        "result": None
    }
    state = "NO_DATA"

    while True:
        print("\n" + msgs["title"])
        for option in msgs["menu"]:
            print(option)

        choice = input(msgs["prompt"]).strip()
        logger.info(f"task4 choice: {choice} (state={state})")

        entry = TRANSITIONS[state].get(choice)
        if not entry:
            print(msgs["invalid_choice"])
            logger.info("task4: неверный пункт меню")
            continue

        if "error" in entry:
            error_type = entry["error"]
            if error_type == "no_data":
                print("Сначала введите все данные!")
            elif error_type == "no_first":
                print("Сначала введите первое число!")
            elif error_type == "no_second":
                print("Сначала введите второе число!")
            elif error_type == "no_operation":
                print("Сначала введите операцию!")
            elif error_type == "no_result":
                print("Сначала выполните вычисление!")
            continue

        action_name = entry.get("action")
        next_state = entry.get("next", state)
        action = ACTION_MAP.get(action_name)
        if action:
            action(state_container)

        if next_state == "BACK":
            return

        state = next_state