"""
Задание 5: Подмассивы с заданной суммой
"""

from exceptions import CalculationError

def execute_5(arr: list, target: int) -> int:
    """Основной алгоритм задания 5"""
    
    try:
        count = 0
        n = len(arr)
        
        for i in range(n):
            current_sum = 0
            for j in range(i, n):
                current_sum += arr[j]
                if current_sum == target:
                    count += 1
        
        return count
    
    except Exception as e:
        raise CalculationError(f"Ошибка вычислений: {e}")