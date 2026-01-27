"""
Задание 5
"""

def execute_5(arr, target):
    """Алгоритм задания 5"""
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
        raise Exception(f"Ошибка вычислений: {e}")