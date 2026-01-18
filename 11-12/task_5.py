"""
Модуль для выполнения задания 5: Подмассивы с заданной суммой.
"""

import logging
from exceptions import InvalidInputError, ValidationError, CalculationError
from messages import COMMON, TASK5

logger = logging.getLogger(__name__)


def validate_array_input(numbers_str: str) -> list[int]:
    """Валидирует ввод массива."""
    if not numbers_str.strip():
        raise InvalidInputError("Ввод не может быть пустым")
    
    try:
        return list(map(int, numbers_str.split()))
    except ValueError:
        raise InvalidInputError("Введены некорректные числа")


def validate_target_sum(target_str: str) -> int:
    """Валидирует целевую сумму."""
    try:
        return int(target_str.strip())
    except ValueError:
        raise ValidationError(TASK5["error_invalid_target"])


def execute_task_5_algorithm(arr: list[int], target_sum: int) -> int:
    """
    Основной алгоритм задания 5.
    
    Args:
        arr: Массив чисел
        target_sum: Целевая сумма
        
    Returns:
        int: Количество подмассивов с заданной суммой
        
    Raises:
        CalculationError: При ошибках вычислений
    """
    logger.info(f"Выполнение алгоритма задания 5: массив={arr}, целевая сумма={target_sum}")
    
    try:
        count = 0
        n = len(arr)
        
        if n == 0:
            logger.warning("Пустой массив")
            return 0
        
        # Перебираем все возможные начала подмассивов
        for i in range(n):
            current_sum = 0
            # Расширяем подмассив от i до конца
            for j in range(i, n):
                current_sum += arr[j]
                
                # Проверка на переполнение (для демонстрации)
                if abs(current_sum) > 10**9:
                    logger.warning(f"Большая промежуточная сумма: {current_sum}")
                
                if current_sum == target_sum:
                    count += 1
                    logger.debug(
                        TASK5["subarray_found"].format(
                            i, j+1, arr[i:j+1]
                        )
                    )
        
        logger.info(f"Алгоритм выполнен. Найдено подмассивов: {count}")
        
        if count == 0:
            logger.info(TASK5["error_no_subarrays"])
        
        return count
        
    except MemoryError:
        raise CalculationError("Недостаточно памяти для обработки большого массива")
    except Exception as e:
        logger.error(f"Ошибка в алгоритме задания 5: {e}", exc_info=True)
        raise CalculationError(f"Ошибка вычислений: {e}")


def run_task5():
    """Основная функция выполнения задания 5."""
    print(f"\n{TASK5['title']}")
    logger.info(TASK5["start"])
    
    try:
        # Ввод массива
        print("Введите массив чисел (через пробел):")
        arr = validate_array_input(input().strip())
        logger.info(f"Введен массив: {arr}")
        
        # Ввод целевой суммы
        target = validate_target_sum(input(TASK5["prompt_target"]).strip())
        logger.info(f"Введена целевая сумма: {target}")
        
        # Выполнение алгоритма
        count = execute_task_5_algorithm(arr, target)
        
        # Вывод результата
        print(TASK5["result"].format(target, count))
        logger.info(TASK5["completed"])
        
    except (InvalidInputError, ValidationError) as e:
        logger.warning(f"Ошибка ввода в задании 5: {e}")
        print(f"\nОшибка ввода: {e}")
    except CalculationError as e:
        logger.error(f"Ошибка вычислений в задании 5: {e}", exc_info=True)
        print(f"\nОшибка вычислений: {e}")
    except Exception as e:
        logger.critical(f"Непредвиденная ошибка в задании 5: {e}", exc_info=True)
        print(f"\nКритическая ошибка: {e}")
        print(COMMON["details_in_log"])