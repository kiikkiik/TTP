"""
Задание 1
"""

def execute_1(arr1, arr2):
    """Алгоритм задания 1"""
    if len(arr1) != len(arr2):
        raise Exception("Массивы должны быть одинаковой длины")
    
    if not arr1 or not arr2:
        raise Exception("Массивы не могут быть пустыми")
    
    a = sorted(arr1, reverse=True)
    b = sorted(arr2)
    
    result = [0 if x == y else x + y for x, y in zip(a, b)]
    return sorted(result)