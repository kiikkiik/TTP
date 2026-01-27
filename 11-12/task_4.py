"""
ЗАДАНИЕ 4: Арифметика чисел-массивов
Алгоритм: преобразование, арифметика, обратное преобразование
"""

from exceptions import CalculationError

def execute_4(arr1: list, arr2: list, operation: str) -> list:
    """
    ОСНОВНОЙ АЛГОРИТМ ЗАДАНИЯ 4
    
    Параметры:
        arr1: list - первое число как массив цифр [1, 2, 3] = 123
        arr2: list - второе число как массив цифр [4, 5, 6] = 456
        operation: str - операция: '+' или '-'
    
    Возвращает:
        list - результат как массив цифр
    
    Вызывает исключения:
        CalculationError - если ошибка вычислений
    """
    
    try:
        # ========== ВСПОМОГАТЕЛЬНАЯ ФУНКЦИЯ ==========
        
        def to_number(arr):
            """
            Преобразует массив цифр в число
            Пример: [1, 2, 3] → 123
            """
            if not arr:  # Если массив пустой
                return 0
            # ''.join(map(str, arr)): [1, 2, 3] → "123"
            # int("123") → 123
            return int(''.join(map(str, arr)))
        
        # ========== ПРЕОБРАЗОВАНИЕ В ЧИСЛА ==========
        
        num1 = to_number(arr1)  # [1, 2, 3] → 123
        num2 = to_number(arr2)  # [4, 5, 6] → 456
        
        # ========== ВЫПОЛНЕНИЕ ОПЕРАЦИИ ==========
        
        if operation == '+':
            result = num1 + num2  # Сложение
        elif operation == '-':
            result = num1 - num2  # Вычитание
        else:
            raise ValueError("Неизвестная операция. Используйте '+' или '-'")
        
        # ========== ОБРАТНОЕ ПРЕОБРАЗОВАНИЕ ==========
        
        if result < 0:
            # Для отрицательных чисел: -123 → ['-', 1, 2, 3]
            return ['-'] + [int(d) for d in str(abs(result))]
        else:
            # Для положительных: 123 → [1, 2, 3]
            # str(result) → "123"
            # for d in "123" → '1', '2', '3'
            # int(d) → 1, 2, 3
            # list(...) → [1, 2, 3]
            return [int(d) for d in str(result)]
    
    except Exception as e:
        raise CalculationError(f"Ошибка вычислений: {e}")