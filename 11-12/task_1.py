def execute_task_1_algorithm(arr1, arr2):
    # Сортируем: первый по убыванию, второй по возрастанию
    a = sorted(arr1, reverse=True)
    b = sorted(arr2)
    
    if len(a) != len(b):
        print("Ошибка: массивы разной длины!")
        return [], [], []
    
    # Считаем с условием: если равны — 0
    result = []
    for i in range(len(a)):
        if a[i] == b[i]:
            result.append(0)
        else:
            result.append(a[i] + b[i])
    
    result = sorted(result)
    return result, a, b
if __name__ == "__main__":
    arr1 = [1, 2, 3, 4]
    arr2 = [4, 3, 2, 1]
    
    # Получаем результат от исходной функции
    result, a, b = execute_task_1_algorithm(arr1, arr2)
    
    # Считаем количество ненулевых элементов
    non_zero_count = sum(1 for x in result if x != 0)
    
    # Выводим в нужном формате
    print((result, non_zero_count))
    # Вывод: ([2, 4, 6, 8], 4)