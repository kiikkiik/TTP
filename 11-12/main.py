"""
Главный модуль программы - консольное приложение для управления заданиями.
"""

import sys
import random
import logging
from task_1 import execute_task_1_algorithm
from task_4 import execute_task_4_algorithm
from task_5 import execute_task_5_algorithm

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler("app.log", encoding='utf-8'),
              logging.StreamHandler()]  # Добавим вывод в консоль тоже
)
logger = logging.getLogger(__name__)

# Глобальные переменные для хранения данных
data1 = None  # Кортеж (arr1, arr2) для задания 1
data4 = None  # Кортеж (arr1, arr2, operation) для задания 4
data5 = None  # Кортеж (arr, target_sum) для задания 5
res1 = None   # Результат задания 1
res4 = None   # Результат задания 4
res5 = None   # Результат задания 5

def input_arr():
    """
    Вводит массив чисел с возможностью ручного или случайного заполнения.
    """
    n = int(input("Размер массива: "))
    way = input("1 - вручную, 2 - случайные числа: ")
    
    logger.info(f"Ввод массива: размер={n}, способ={way}")
    
    if way == "2":
        arr = [random.randint(-10, 10) for _ in range(n)]
        logger.info(f"Сгенерирован случайный массив: {arr}")
        return arr
    else:
        user_input = input("Введите числа через пробел: ")
        arr = list(map(int, user_input.split()))
        logger.info(f"Введен массив вручную: {arr}")
        return arr

def task1():
    """Выполняет задание 1 через консольный интерфейс."""
    global data1, res1
    
    logger.info("Начало выполнения задания 1")
    print("\n--- Задание 1: Обработка двух массивов ---")
    
    print("Введите первый массив:")
    a = input_arr()
    print("Введите второй массив:")
    b = input_arr()
    
    data1 = (a, b)
    logger.info(f"Вызов функции execute_task_1_algorithm с параметрами: arr1={a}, arr2={b}")
    
    # Используем копии массивов, чтобы не изменять оригиналы
    res1, s1, s2 = execute_task_1_algorithm(a.copy(), b.copy())
    
    logger.info(f"Задание 1 выполнено. Результат: {res1}")
    
    print("\nРезультаты:")
    print(f"Отсортированный первый массив (по убыванию): {s1}")
    print(f"Отсортированный второй массив (по возрастанию): {s2}")
    print(f"Итоговый массив: {res1}")

def task4():
    """Выполняет задание 4 через консольный интерфейс."""
    global data4, res4
    
    logger.info("Начало выполнения задания 4")
    print("\n--- Задание 4: Арифметика чисел-массивов ---")
    
    print("Введите первое число (цифры через пробел):")
    a_input = input()
    a = list(map(int, a_input.split()))
    
    print("Введите второе число (цифры через пробел):")
    b_input = input()
    b = list(map(int, b_input.split()))
    
    op = input("Операция (+ или -): ")
    
    logger.info(f"Ввод для задания 4: a={a}, b={b}, операция={op}")
    data4 = (a, b, op)
    
    logger.info(f"Вызов функции execute_task_4_algorithm с параметрами: arr1={a}, arr2={b}, operation={op}")
    res4 = execute_task_4_algorithm(a, b, op)
    logger.info(f"Задание 4 выполнено. Результат: {res4}")
    
    # Форматируем вывод: заменяем дефис на минус для читаемости
    if isinstance(res4[0], str) and res4[0] == '-':
        formatted_result = "−" + "".join(map(str, res4[1:]))
    else:
        formatted_result = "".join(map(str, res4))
    
    print(f"Результат: {formatted_result}")

def task5():
    """Выполняет задание 5 через консольный интерфейс."""
    global data5, res5
    
    logger.info("Начало выполнения задания 5")
    print("\n--- Задание 5: Подмассивы с заданной суммой ---")
    
    arr = input_arr()
    target = int(input("Целевая сумма: "))
    
    logger.info(f"Ввод для задания 5: массив={arr}, целевая сумма={target}")
    data5 = (arr, target)
    
    logger.info(f"Вызов функции execute_task_5_algorithm с параметрами: arr={arr}, target_sum={target}")
    res5 = execute_task_5_algorithm(arr, target)
    logger.info(f"Задание 5 выполнено. Количество подмассивов: {res5}")
    
    print(f"Количество подмассивов с суммой {target}: {res5}")



def main_menu():
    """Главное меню программы."""
    logger.info("=" * 50)
    logger.info("ПРОГРАММА ЗАПУЩЕНА")
    logger.info("=" * 50)
    
    print("=" * 50)
    print("ПРОГРАММА ДЛЯ ВЫПОЛНЕНИЯ ЗАДАНИЙ")
    print("Логирование включено. Логи сохраняются в app.log")
    print("Текущий уровень логирования: INFO")
    print("=" * 50)
    
    while True:
        print("\n" + "="*50)
        print("ГЛАВНОЕ МЕНЮ")
        print("1. Задание 1: Обработка двух массивов")
        print("4. Задание 4: Арифметика чисел-массивов")
        print("5. Задание 5: Подмассивы с заданной суммой")
        print("h. Справка")
        print("l. Изменить уровень логирования")
        print("0. Выход")
        choice = input("Выберите пункт меню: ").strip()
        
        if choice == '1':
            logger.info("Выбрано задание 1. Обработка двух массивов.")
            task1()
        elif choice == '4':
            logger.info("Выбрано задание 4. Арифметика чисел-массивов.")
            task4()
        elif choice == '5':
            logger.info("Выбрано задание 5. Подмассивы с заданной суммой.")
            task5()
        elif choice.lower() == 'h':
            logger.info("Выбрана справка.")
        elif choice.lower() == 'l':
            logger.info("Выбрано изменение уровня логирования.")
        elif choice == '0':
            logger.info("Выбран выход из программы.")
            print("Выход из программы.")
            break
        else:
            logger.warning(f"Неверный выбор в меню: {choice}")
            print("Неверный выбор. Введите 'h' для справки.")

# Точка входа в программу
if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        logger.info("Программа прервана пользователем (Ctrl+C)")
        print("\n\nПрограмма прервана пользователем.")
        sys.exit()
    except Exception as e:
        logger.error(f"Неожиданная ошибка в main: {e}", exc_info=True)
        print(f"\nПроизошла ошибка: {e}")
        print("Подробности в лог-файле.")