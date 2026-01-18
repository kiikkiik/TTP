"""
Модуль для выполнения задания 4: Арифметика чисел-массивов.
"""

import logging
from exceptions import (
    CalculationError, InvalidArrayError, EmptyArrayError, InvalidNumberError,
    UnsupportedOperationError, NegativeResultError, ValidationError
)
from messages import COMMON, TASK4

logger = logging.getLogger(__name__)


def validate_digits_array(input_str: str) -> list[int]:
    """Валидирует массив цифр."""
    if not input_str.strip():
        raise EmptyArrayError(TASK4["error_empty_input"])
    
    try:
        digits = list(map(int, input_str.split()))
        
        # Проверяем, что все числа - цифры (0-9)
        for digit in digits:
            if not (0 <= digit <= 9):
                raise InvalidNumberError(TASK4["error_invalid_digit"])
        
        return digits
    except ValueError:
        raise InvalidArrayError(TASK4["error_invalid_number"])


def validate_operation(op: str) -> str:
    """Валидирует операцию."""
    op = op.strip()
    if op not in ['+', '-']:
        raise UnsupportedOperationError(TASK4["error_invalid_operation"])
    return op


def digits_to_number(digits: list[int]) -> int:
    """Преобразует массив цифр в число."""
    if not digits:
        return 0
    return int(''.join(map(str, digits)))


def number_to_digits(number: int) -> list[int]:
    """Преобразует число в массив цифр."""
    if number == 0:
        return [0]
    
    if number < 0:
        # Для отрицательных чисел возвращаем список с минусом в начале
        return ['-'] + [int(d) for d in str(abs(number))]
    
    return [int(d) for d in str(number)]


def execute_task_4_algorithm(arr1: list[int], arr2: list[int], operation: str) -> list:
    """
    Основной алгоритм задания 4.
    
    Args:
        arr1: Первое число в виде массива цифр
        arr2: Второе число в виде массива цифр
        operation: Операция '+' или '-'
        
    Returns:
        list: Результат в виде массива цифр (или ['-', ...] для отрицательных)
        
    Raises:
        CalculationError: При ошибках вычислений
        NegativeResultError: Если результат отрицательный (только для демонстрации)
    """
    logger.info(f"Выполнение алгоритма задания 4: {arr1} {operation} {arr2}")
    
    try:
        # Преобразуем массивы в числа
        num1 = digits_to_number(arr1)
        num2 = digits_to_number(arr2)
        
        # Выполняем операцию
        if operation == '+':
            result = num1 + num2
        else:  # operation == '-'
            result = num1 - num2
            
            # Для демонстрации обработки отрицательных результатов
            if result < 0:
                raise NegativeResultError(
                    TASK4["error_negative_result"].format(result)
                )
        
        # Преобразуем результат обратно в массив цифр
        if result < 0:
            result_digits = ['-'] + [int(d) for d in str(abs(result))]
        else:
            result_digits = number_to_digits(result)
        
        logger.info(f"Алгоритм выполнен. Результат: {result_digits}")
        return result_digits
        
    except OverflowError:
        raise CalculationError("Переполнение при вычислениях")
    except Exception as e:
        logger.error(f"Ошибка в алгоритме задания 4: {e}", exc_info=True)
        raise CalculationError(f"Ошибка вычислений: {e}")


def run_task4():
    """Основная функция выполнения задания 4."""
    print(f"\n{TASK4['title']}")
    logger.info(TASK4["start"])
    
    try:
        # Ввод первого числа
        arr1 = validate_digits_array(input(TASK4["prompt_a"]).strip())
        logger.info(f"Введено первое число: {arr1}")
        
        # Ввод второго числа
        arr2 = validate_digits_array(input(TASK4["prompt_b"]).strip())
        logger.info(f"Введено второе число: {arr2}")
        
        # Ввод операции
        operation = validate_operation(input(TASK4["prompt_op"]).strip())
        logger.info(f"Выбрана операция: {operation}")
        
        # Выполнение алгоритма
        result = execute_task_4_algorithm(arr1, arr2, operation)
        
        # Вывод результата
        if isinstance(result[0], str) and result[0] == '-':
            formatted_result = "−" + "".join(map(str, result[1:]))
        else:
            formatted_result = "".join(map(str, result))
        
        print(TASK4["result"].format(formatted_result))
        logger.info(TASK4["completed"])
        
    except (EmptyArrayError, InvalidArrayError, InvalidNumberError) as e:
        logger.warning(f"Ошибка ввода в задании 4: {e}")
        print(f"\nОшибка ввода: {e}")
    except UnsupportedOperationError as e:
        logger.warning(f"Ошибка операции в задании 4: {e}")
        print(f"\nОшибка: {e}")
    except NegativeResultError as e:
        logger.warning(f"Отрицательный результат в задании 4: {e}")
        print(f"\nОшибка: {e}")
    except (ValidationError, CalculationError) as e:
        logger.error(f"Ошибка вычислений в задании 4: {e}", exc_info=True)
        print(f"\nОшибка вычислений: {e}")
    except Exception as e:
        logger.critical(f"Непредвиденная ошибка в задании 4: {e}", exc_info=True)
        print(f"\nКритическая ошибка: {e}")
        print(COMMON["details_in_log"])