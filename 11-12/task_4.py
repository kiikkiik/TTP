def execute_task_4_algorithm(arr1, arr2, operation='+'):
    # Преобразуем массивы в числа
    num1 = int("".join(map(str, arr1)))
    num2 = int("".join(map(str, arr2)))
    
    if operation == '+':
        res = num1 + num2
    elif operation == '-':
        res = num1 - num2
    else:
        return ["Ошибка"]
    
    # Если отрицательное — добавляем минус
    if res < 0:
        return ['-', *list(map(int, str(-res)))]
    else:
        return list(map(int, str(res)))
if __name__ == "__main__":
    # Пример 1: Сложение
    arr1 = [1, 2, 3]
    arr2 = [4, 5]
    print(execute_task_4_algorithm(arr1, arr2, '+'))
    # Вывод: ([1, 6, 8], 3)
    
    # Пример 2: Вычитание с отрицательным результатом
    arr3 = [1, 0, 0]
    arr4 = [5, 0]
    print(execute_task_4_algorithm(arr3, arr4, '-'))
    # Вывод: (['-', 5, 0], 3)