"""
ЗАДАНИЕ 1: Обработка двух массивов
Алгоритм: сортировка и поэлементное сложение
"""

from exceptions import ValidationError, CalculationError

def execute_1(arr1: list, arr2: list) -> list:
    """
    ОСНОВНОЙ АЛГОРИТМ ЗАДАНИЯ 1
    
    Параметры:
        arr1: list - первый массив чисел
        arr2: list - второй массив чисел
    
    Возвращает:
        list - обработанный массив
    
    Вызывает исключения:
        ValidationError - если данные невалидны
        CalculationError - если ошибка вычислений
    """
    
    # ========== ВАЛИДАЦИЯ ВХОДНЫХ ДАННЫХ ==========
    
    # Проверка одинаковой длины массивов
    if len(arr1) != len(arr2):
        raise ValidationError("Массивы должны быть одинаковой длины")
    
    # Проверка на пустые массивы
    if not arr1 or not arr2:
        raise ValidationError("Массивы не могут быть пустыми")
    
    # ========== ВЫЧИСЛИТЕЛЬНАЯ ЧАСТЬ ==========
    
    try:
        # 1. СОРТИРОВКА ПЕРВОГО МАССИВА ПО УБЫВАНИЮ
        # sorted() возвращает новый отсортированный список
        # reverse=True - сортировка по убыванию
        a = sorted(arr1, reverse=True)
        
        # 2. СОРТИРОВКА ВТОРОГО МАССИВА ПО ВОЗРАСТАНИЮ
        # По умолчанию sorted() сортирует по возрастанию
        b = sorted(arr2)
        
        # 3. ПОЭЛЕМЕНТНОЕ СРАВНЕНИЕ И СЛОЖЕНИЕ
        result = []
        for i in range(len(a)):
            if a[i] == b[i]:
                # Если элементы равны - добавляем 0
                result.append(0)
            else:
                # Иначе - сумму элементов
                result.append(a[i] + b[i])
        
        # 4. СОРТИРОВКА РЕЗУЛЬТАТА ПО ВОЗРАСТАНИЮ
        return sorted(result)
    
    except Exception as e:
        # Любая ошибка преобразуется в CalculationError
        raise CalculationError(f"Ошибка вычислений: {e}")