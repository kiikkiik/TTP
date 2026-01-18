"""
Модуль для выполнения задания 1: Обработка двух массивов.
"""

import logging
from exceptions import (
    InvalidArrayError, EmptyArrayError, ArrayLengthMismatchError, 
    ValidationError, CalculationError
)
from messages import COMMON, TASK1

logger = logging.getLogger(__name__)


def validate_array_size(size: str) -> int:
    """Валидирует размер массива."""
    try:
        size_int = int(size)
        if size_int <= 0:
            raise ValidationError(TASK1["error_invalid_size"])
        return size_int
    except ValueError:
        raise ValidationError(TASK1["error_invalid_size"])


def validate_array_numbers(numbers_str: str, expected_size: int) -> list[int]:
    """Валидирует и преобразует строку чисел в массив."""
    if not numbers_str.strip():
        raise EmptyArrayError(TASK1["error_empty_array"])
    
    try:
        numbers = list(map(int, numbers_str.split()))
        
        # Проверяем размер (предупреждение, но не ошибка)
        if len(numbers) != expected_size:
            logger.warning(f"Ожидалось {expected_size} чисел, получено {len(numbers)}")
        
        return numbers
    except ValueError:
        raise InvalidArrayError(TASK1["error_invalid_numbers"])


def generate_random_array(size: int) -> list[int]:
    """Генерирует случайный массив."""
    import random
    return [random.randint(-10, 10) for _ in range(size)]


def execute_task_1_algorithm(arr1: list[int], arr2: list[int]) -> tuple:
    """
    Основной алгоритм задания 1.
    
    Args:
        arr1: Первый массив
        arr2: Второй массив
        
    Returns:
        tuple: (результат, отсортированный arr1, отсортированный arr2)
        
    Raises:
        ArrayLengthMismatchError: Если массивы разной длины
        CalculationError: При ошибках вычислений
    """
    logger.info(f"Выполнение алгоритма задания 1: arr1={arr1}, arr2={arr2}")
    
    # Проверка длины массивов
    if len(arr1) != len(arr2):
        error_msg = TASK1["error_length_mismatch"].format(len(arr1), len(arr2))
        raise ArrayLengthMismatchError(error_msg)
    
    # Проверка на пустые массивы
    if not arr1 or not arr2:
        raise EmptyArrayError(TASK1["error_empty_array"])
    
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
                # Проверка на возможное переполнение
                try:
                    sum_val = a[i] + b[i]
                    # Проверка на слишком большие числа (для демонстрации)
                    if abs(sum_val) > 10**9:
                        logger.warning(f"Большая сумма: {sum_val}")
                    result.append(sum_val)
                except OverflowError:
                    raise CalculationError(TASK1["error_array_too_large"])
        
        result = sorted(result)
        logger.info(f"Алгоритм выполнен. Результат: {result}")
        
        return result, a, b
        
    except Exception as e:
        logger.error(f"Ошибка в алгоритме задания 1: {e}", exc_info=True)
        raise CalculationError(f"Ошибка вычислений: {e}")


def run_task1():
    """Основная функция выполнения задания 1."""
    print(f"\n{TASK1['title']}")
    logger.info(TASK1["start"])
    
    try:
        # Ввод размера и способа для первого массива
        print(TASK1["prompt_array1"])
        size1 = validate_array_size(input(TASK1["prompt_size"]).strip())
        method1 = input(TASK1["prompt_method"]).strip()
        
        if method1 == "2":
            arr1 = generate_random_array(size1)
            logger.info(f"Сгенерирован случайный массив 1: {arr1}")
        else:
            arr1 = validate_array_numbers(
                input(TASK1["prompt_manual"]).strip(),
                size1
            )
            logger.info(f"Введен массив 1 вручную: {arr1}")
        
        # Ввод размера и способа для второго массива
        print(TASK1["prompt_array2"])
        size2 = validate_array_size(input(TASK1["prompt_size"]).strip())
        method2 = input(TASK1["prompt_method"]).strip()
        
        if method2 == "2":
            arr2 = generate_random_array(size2)
            logger.info(f"Сгенерирован случайный массив 2: {arr2}")
        else:
            arr2 = validate_array_numbers(
                input(TASK1["prompt_manual"]).strip(),
                size2
            )
            logger.info(f"Введен массив 2 вручную: {arr2}")
        
        # Выполнение алгоритма
        result, sorted1, sorted2 = execute_task_1_algorithm(arr1, arr2)
        
        # Вывод результатов
        print("\nРезультаты:")
        print(TASK1["result_sorted1"].format(sorted1))
        print(TASK1["result_sorted2"].format(sorted2))
        print(TASK1["result_final"].format(result))
        
        logger.info(TASK1["completed"])
        
    except (ValidationError, InvalidArrayError, EmptyArrayError) as e:
        logger.warning(f"Ошибка ввода в задании 1: {e}")
        print(f"\nОшибка ввода: {e}")
    except ArrayLengthMismatchError as e:
        logger.warning(f"Ошибка данных в задании 1: {e}")
        print(f"\nОшибка: {e}")
    except CalculationError as e:
        logger.error(f"Ошибка вычислений в задании 1: {e}", exc_info=True)
        print(f"\nОшибка вычислений: {e}")
    except Exception as e:
        logger.critical(f"Непредвиденная ошибка в задании 1: {e}", exc_info=True)
        print(f"\nКритическая ошибка: {e}")
        print(COMMON["details_in_log"])