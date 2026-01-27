"""
Task 1 — обработка двух массивов (FSM-меню)
"""

import random
import logging
from exceptions import (
    InvalidArrayError, EmptyArrayError, ArrayLengthMismatchError, 
    ValidationError, CalculationError
)
from messages import MESSAGES

logger = logging.getLogger(__name__)
msgs = MESSAGES["task1"]

# Вспомогательные функции

def generate_array(size: int) -> list[int]:
    """Генерирует случайный массив."""
    if size <= 0:
        raise ValidationError("Размер массива должен быть положительным")
    return [random.randint(-10, 10) for _ in range(size)]


def input_array_manual() -> list[int]:
    """Ввод массива чисел вручную."""
    raw = input("Введите числа через пробел: ")
    if not raw.strip():
        raise InvalidArrayError("Пустой ввод")
    try:
        return [int(x) for x in raw.split()]
    except ValueError:
        raise InvalidArrayError("Введены некорректные числа")


def execute_task_1_algorithm(arr1: list[int], arr2: list[int]) -> tuple:
    """Основной алгоритм задания 1."""
    if len(arr1) != len(arr2):
        error_msg = "Массивы должны быть одинаковой длины. Длина первого: {}, второго: {}".format(
            len(arr1), len(arr2))
        raise ArrayLengthMismatchError(error_msg)
    
    if not arr1 or not arr2:
        raise EmptyArrayError("Массив не может быть пустым")
    
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
        raise CalculationError(f"Ошибка вычислений: {e}")


# ОБРАБОТЧИКИ ДЕЙСТВИЙ FSM

def _input_arrays(state_container):
    """Ввод двух массивов вручную."""
    try:
        print("Первый массив:")
        arr1 = input_array_manual()
        print("Второй массив:")
        arr2 = input_array_manual()
        state_container["arr1"], state_container["arr2"], state_container["result"] = arr1, arr2, None
        state_container["sorted1"], state_container["sorted2"] = None, None
        logger.info("task1: массивы введены вручную")
    except Exception as e:
        logger.error(str(e))
        print(msgs["input_error"])


def _generate_arrays(state_container):
    """Генерация двух случайных массивов."""
    try:
        size1 = int(input("Размер первого массива: "))
        size2 = int(input("Размер второго массива: "))
        arr1 = generate_array(size1)
        arr2 = generate_array(size2)
        state_container["arr1"], state_container["arr2"], state_container["result"] = arr1, arr2, None
        state_container["sorted1"], state_container["sorted2"] = None, None
        print("Первый массив:", arr1)
        print("Второй массив:", arr2)
        logger.info("task1: массивы сгенерированы")
    except Exception as e:
        logger.error(str(e))
        print(msgs["input_error"])


def _perform_algorithm(state_container):
    """Выполняет алгоритм."""
    arr1 = state_container.get("arr1")
    arr2 = state_container.get("arr2")

    if arr1 is None or arr2 is None:
        print(msgs["no_data"])
        logger.warning("task1: попытка выполнения без данных")
        return

    try:
        result, sorted1, sorted2 = execute_task_1_algorithm(arr1, arr2)
        state_container["result"] = result
        state_container["sorted1"], state_container["sorted2"] = sorted1, sorted2
        print(msgs["calculation_done"])
        logger.info("task1: алгоритм выполнен")
    except Exception as e:
        logger.error(str(e))
        print(msgs["no_data"])


def _show_result(state_container):
    """Показывает результат."""
    result = state_container.get("result")
    sorted1 = state_container.get("sorted1")
    sorted2 = state_container.get("sorted2")

    if result is None:
        print(msgs["no_data"])
        logger.warning("task1: попытка показать результат без вычислений")
    else:
        print("\nРезультаты:")
        print(f"Отсортированный первый массив (по убыванию): {sorted1}")
        print(f"Отсортированный второй массив (по возрастанию): {sorted2}")
        print(f"Итоговый массив: {result}")
        logger.info("task1: результат показан")


def _disable_logging(state_container):
    """Отключает логирование."""
    logger.setLevel("CRITICAL")
    print("Логирование отключено")
    logger.critical("task1: логирование отключено")


def _back(state_container):
    """Возвращает в главное меню."""
    logger.info("task1: возврат в главное меню")


# ACTION MAP - словарь действий

ACTION_MAP = {
    "input_arrays": _input_arrays,
    "generate_arrays": _generate_arrays,
    "perform_algorithm": _perform_algorithm,
    "show_result": _show_result,
    "disable_logging": _disable_logging,
    "back": _back
}

# FSM TRANSITIONS - переходы автомата

TRANSITIONS = {
    "NO_DATA": {
        "1": {"action": "input_arrays", "next": "HAS_DATA"},
        "2": {"action": "generate_arrays", "next": "HAS_DATA"},
        "3": {"error": "no_data"},
        "4": {"error": "no_result"},
        "5": {"action": "back", "next": "BACK"},
        "6": {"action": "disable_logging", "next": "NO_DATA"},
    },
    "HAS_DATA": {
        "1": {"action": "input_arrays", "next": "HAS_DATA"},
        "2": {"action": "generate_arrays", "next": "HAS_DATA"},
        "3": {"action": "perform_algorithm", "next": "HAS_RESULT"},
        "4": {"error": "no_result"},
        "5": {"action": "back", "next": "BACK"},
        "6": {"action": "disable_logging", "next": "HAS_DATA"},
    },
    "HAS_RESULT": {
        "1": {"action": "input_arrays", "next": "HAS_DATA"},
        "2": {"action": "generate_arrays", "next": "HAS_DATA"},
        "3": {"action": "perform_algorithm", "next": "HAS_RESULT"},
        "4": {"action": "show_result", "next": "HAS_RESULT"},
        "5": {"action": "back", "next": "BACK"},
        "6": {"action": "disable_logging", "next": "HAS_RESULT"},
    }
}

# ГЛАВНАЯ ФУНКЦИЯ МЕНЮ

def task1_menu():
    """Запускает FSM-меню задачи 1."""
    state_container = {
        "arr1": None,
        "arr2": None,
        "sorted1": None,
        "sorted2": None,
        "result": None
    }
    state = "NO_DATA"

    while True:
        print("\n" + msgs["title"])
        for option in msgs["menu"]:
            print(option)

        choice = input(msgs["prompt"]).strip()
        logger.info(f"task1 choice: {choice} (state={state})")

        entry = TRANSITIONS[state].get(choice)
        if not entry:
            print(msgs["invalid_choice"])
            logger.info("task1: неверный пункт меню")
            continue

        if "error" in entry:
            if entry["error"] == "no_data":
                print(msgs["no_data"])
                logger.warning("task1: попытка действия без данных")
            elif entry["error"] == "no_result":
                print(msgs["no_data"])
                logger.warning("task1: попытка показать результат без вычислений")
            continue

        action_name = entry.get("action")
        next_state = entry.get("next", state)
        action = ACTION_MAP.get(action_name)
        if action:
            action(state_container)

        if next_state == "BACK":
            return

        state = next_state