import sys
import random
from task_1 import execute_task_1_algorithm
from task_4 import execute_task_4_algorithm
from task_5 import execute_task_5_algorithm

# Глобальные переменные для хранения данных
data1 = None
data4 = None
data5 = None
res1 = None
res4 = None
res5 = None

def menu():
    print("\n=== ГЛАВНОЕ МЕНЮ ===")
    print("1. Задание 1")
    print("4. Задание 4")
    print("5. Задание 5")
    print("0. Выход")
    return input("Выбери: ")

def input_arr():
    n = int(input("Размер массива: "))
    way = input("1 - вручную, 2 - рандом: ")
    if way == "2":
        return [random.randint(-10,10) for _ in range(n)]
    else:
        return list(map(int, input("Введи числа через пробел: ").split()))

# Задание 1
def task1():
    global data1, res1
    print("\n--- Задание 1 ---")
    a = input_arr()
    b = input_arr()
    data1 = (a, b)
    res1, s1, s2 = execute_task_1_algorithm(a.copy(), b.copy())
    print("Отсортированный arr1 (убыв):", s1)
    print("Отсортированный arr2 (возр):", s2)
    print("Результат:", res1)

# Задание 4
def task4():
    global data4, res4
    print("\n--- Задание 4 ---")
    print("Ввод первого числа (цифры через пробел):")
    a = list(map(int, input().split()))
    print("Ввод второго числа:")
    b = list(map(int, input().split()))
    op = input("Операция + или -: ")
    data4 = (a, b, op)
    res4 = execute_task_4_algorithm(a, b, op)
    print("Результат:", "".join(map(str, res4)).replace("-","−") if isinstance(res4[0], str) else "".join(map(str,res4)))

# Задание 5
def task5():
    global data5, res5
    print("\n--- Задание 5 ---")
    arr = input_arr()
    target = int(input("Целевая сумма: "))
    data5 = (arr, target)
    res5 = execute_task_5_algorithm(arr, target)
    print(f"Подмассивов с суммой {target}: {res5}")

# Основной цикл
while True:
    choice = menu()
    if choice == "1":
        task1()
    elif choice == "4":
        task4()
    elif choice == "5":
        task5()
    elif choice == "0":
        print("Пока!")
        sys.exit()
    else:
        print("Такого пункта нет!")