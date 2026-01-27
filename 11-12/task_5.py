"""
Task 5 — подмассивы с заданной суммой (FSM-меню)
"""

import logging
from messages import MESSAGES

logger = logging.getLogger(__name__)
msgs = MESSAGES["task5"]

# Вспомогательные функции

def input_array_manual() -> list[int]:
    """Ввод массива чисел вручную."""
    raw = input("Введите числа через пробел: ")
    if not raw.strip():
        raise ValueError("Пустой ввод")
    try:
        return [int(x) for x in raw.split()]
    except ValueError:
        raise ValueError("Введены нецелые числа")


def input_target_sum() -> int:
    """Ввод целевой суммы."""
    raw = input("Введите целевую сумму: ").strip()
    try:
        return int(raw)
    except ValueError:
        raise ValueError("Целевая сумма должна быть целым числом")


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


# ОБРАБОТЧИКИ ДЕЙСТВИЙ FSM

def _input_array(state_container):
    """Ввод массива."""
    try:
        arr = input_array_manual()
        state_container["arr"] = arr
        state_container["count"] = None
        logger.info("task5: массив введен")
    except Exception as e:
        logger.error(str(e))
        print(msgs["input_error"])


def _input_target(state_container):
    """Ввод целевой суммы."""
    try:
        target = input_target_sum()
        state_container["target"] = target
        state_container["count"] = None
        logger.info("task5: целевая сумма введена")
    except Exception as e:
        logger.error(str(e))
        print(msgs["input_error"])


def _find_subarrays(state_container):
    """Поиск подмассивов."""
    arr = state_container.get("arr")
    target = state_container.get("target")

    if arr is None or target is None:
        print(msgs["no_data"])
        logger.warning("task5: попытка поиска без данных")
        return

    try:
        count = execute_task_5_algorithm(arr, target)
        state_container["count"] = count
        print(msgs["calculation_done"])
        logger.info("task5: поиск подмассивов выполнен")
    except Exception as e:
        logger.error(str(e))
        print(msgs["no_data"])


def _show_result(state_container):
    """Показывает результат."""
    count = state_container.get("count")
    arr = state_container.get("arr")
    target = state_container.get("target")

    if count is None:
        print(msgs["no_data"])
        logger.warning("task5: попытка показать результат без вычислений")
    else:
        print(f"\nМассив: {arr}")
        print(f"Целевая сумма: {target}")
        print(f"Количество подмассивов с суммой {target}: {count}")
        logger.info("task5: результат показан")


def _disable_logging(state_container):
    """Отключает логирование."""
    logger.setLevel("CRITICAL")
    print("Логирование отключено")
    logger.critical("task5: логирование отключено")


def _back(state_container):
    """Возвращает в главное меню."""
    logger.info("task5: возврат в главное меню")


# ACTION MAP

ACTION_MAP = {
    "input_array": _input_array,
    "input_target": _input_target,
    "find_subarrays": _find_subarrays,
    "show_result": _show_result,
    "disable_logging": _disable_logging,
    "back": _back
}

# FSM TRANSITIONS

TRANSITIONS = {
    "NO_DATA": {
        "1": {"action": "input_array", "next": "HAS_ARRAY"},
        "2": {"error": "no_array"},
        "3": {"error": "no_data"},
        "4": {"error": "no_result"},
        "5": {"action": "back", "next": "BACK"},
        "6": {"action": "disable_logging", "next": "NO_DATA"},
    },
    "HAS_ARRAY": {
        "1": {"action": "input_array", "next": "HAS_ARRAY"},
        "2": {"action": "input_target", "next": "READY"},
        "3": {"error": "no_target"},
        "4": {"error": "no_result"},
        "5": {"action": "back", "next": "BACK"},
        "6": {"action": "disable_logging", "next": "HAS_ARRAY"},
    },
    "READY": {
        "1": {"action": "input_array", "next": "HAS_ARRAY"},
        "2": {"action": "input_target", "next": "READY"},
        "3": {"action": "find_subarrays", "next": "HAS_RESULT"},
        "4": {"error": "no_result"},
        "5": {"action": "back", "next": "BACK"},
        "6": {"action": "disable_logging", "next": "READY"},
    },
    "HAS_RESULT": {
        "1": {"action": "input_array", "next": "HAS_ARRAY"},
        "2": {"action": "input_target", "next": "READY"},
        "3": {"action": "find_subarrays", "next": "HAS_RESULT"},
        "4": {"action": "show_result", "next": "HAS_RESULT"},
        "5": {"action": "back", "next": "BACK"},
        "6": {"action": "disable_logging", "next": "HAS_RESULT"},
    }
}

# ГЛАВНАЯ ФУНКЦИЯ МЕНЮ

def task5_menu():
    """Запускает FSM-меню задачи 5."""
    state_container = {
        "arr": None,
        "target": None,
        "count": None
    }
    state = "NO_DATA"

    while True:
        print("\n" + msgs["title"])
        for option in msgs["menu"]:
            print(option)

        choice = input(msgs["prompt"]).strip()
        logger.info(f"task5 choice: {choice} (state={state})")

        entry = TRANSITIONS[state].get(choice)
        if not entry:
            print(msgs["invalid_choice"])
            logger.info("task5: неверный пункт меню")
            continue

        if "error" in entry:
            error_type = entry["error"]
            if error_type == "no_data":
                print("Сначала введите все данные!")
            elif error_type == "no_array":
                print("Сначала введите массив!")
            elif error_type == "no_target":
                print("Сначала введите целевую сумму!")
            elif error_type == "no_result":
                print("Сначала выполните поиск подмассивов!")
            continue

        action_name = entry.get("action")
        next_state = entry.get("next", state)
        action = ACTION_MAP.get(action_name)
        if action:
            action(state_container)

        if next_state == "BACK":
            return

        state = next_state