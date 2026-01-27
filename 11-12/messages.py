"""
messages.py

Централизованный словарь сообщений для всего приложения.
"""

class Messages:
    """Централизованные сообщения для всех меню и FSM."""

    class MENU_MAIN:
        title = "=== ГЛАВНОЕ МЕНЮ ==="
        options = [
            "1. Задание 1: Обработка двух массивов",
            "4. Задание 4: Арифметика чисел-массивов", 
            "5. Задание 5: Подмассивы с заданной суммой",
            "h. Справка",
            "l. Изменить уровень логирования",
            "0. Выход"
        ]
        prompt = "Выберите пункт: "
        invalid = "Неверный пункт! Введите 'h' для справки."
        exit_msg = "Выход из программы..."

    class TASK1:
        title = "=== ЗАДАНИЕ 1: Обработка двух массивов ==="
        menu = [
            "1. Ввести массивы вручную",
            "2. Сгенерировать массивы случайно",
            "3. Выполнить алгоритм (сортировка и сложение)",
            "4. Показать результат",
            "5. Назад в главное меню",
            "6. Отключить логирование"
        ]
        prompt = "Выберите пункт: "
        input_error = "Ошибка ввода массивов!"
        calculation_done = "Алгоритм выполнен."
        no_data = "Сначала введите массивы!"
        invalid_choice = "Неверный пункт!"

    class TASK4:
        title = "=== ЗАДАНИЕ 4: Арифметика чисел-массивов ==="
        menu = [
            "1. Ввести первое число (цифры через пробел)",
            "2. Ввести второе число (цифры через пробел)",
            "3. Ввести операцию (+ или -)",
            "4. Выполнить вычисление",
            "5. Показать результат",
            "6. Назад в главное меню",
            "7. Отключить логирование"
        ]
        prompt = "Выберите пункт: "
        input_error = "Ошибка ввода!"
        calculation_done = "Вычисление выполнено."
        no_data = "Сначала введите данные!"
        invalid_choice = "Неверный пункт!"

    class TASK5:
        title = "=== ЗАДАНИЕ 5: Подмассивы с заданной суммой ==="
        menu = [
            "1. Ввести массив",
            "2. Ввести целевую сумму",
            "3. Найти подмассивы",
            "4. Показать результат",
            "5. Назад в главное меню",
            "6. Отключить логирование"
        ]
        prompt = "Выберите пункт: "
        input_error = "Ошибка ввода!"
        calculation_done = "Поиск подмассивов выполнен."
        no_data = "Сначала введите данные!"
        invalid_choice = "Неверный пункт!"

# Совместимость со старым стилем
MESSAGES = {
    "main_menu": {
        "title": Messages.MENU_MAIN.title,
        "options": Messages.MENU_MAIN.options,
        "prompt": Messages.MENU_MAIN.prompt,
        "invalid": Messages.MENU_MAIN.invalid,
        "exit": Messages.MENU_MAIN.exit_msg
    },
    "task1": {
        "title": Messages.TASK1.title,
        "menu": Messages.TASK1.menu,
        "prompt": Messages.TASK1.prompt,
        "input_error": Messages.TASK1.input_error,
        "calculation_done": Messages.TASK1.calculation_done,
        "no_data": Messages.TASK1.no_data,
        "invalid_choice": Messages.TASK1.invalid_choice
    },
    "task4": {
        "title": Messages.TASK4.title,
        "menu": Messages.TASK4.menu,
        "prompt": Messages.TASK4.prompt,
        "input_error": Messages.TASK4.input_error,
        "calculation_done": Messages.TASK4.calculation_done,
        "no_data": Messages.TASK4.no_data,
        "invalid_choice": Messages.TASK4.invalid_choice
    },
    "task5": {
        "title": Messages.TASK5.title,
        "menu": Messages.TASK5.menu,
        "prompt": Messages.TASK5.prompt,
        "input_error": Messages.TASK5.input_error,
        "calculation_done": Messages.TASK5.calculation_done,
        "no_data": Messages.TASK5.no_data,
        "invalid_choice": Messages.TASK5.invalid_choice
    }
}

# Старые сообщения для совместимости
COMMON = {
    "program_start": "Программа запущена",
    "program_exit": "Выход из программы",
    "program_interrupted": "Программа прервана пользователем",
    "unexpected_error": "Произошла непредвиденная ошибка: {}",
    "details_in_log": "Подробности в лог-файле.",
}

MENU = {
    "title": "ГЛАВНОЕ МЕНЮ",
    "task1": "Задание 1: Обработка двух массивов",
    "task4": "Задание 4: Арифметика чисел-массивов",
    "task5": "Задание 5: Подмассивы с заданной суммой",
    "help": "Справка",
    "logging": "Изменить уровень логирования",
    "exit": "Выход",
    "prompt_choice": "Выберите пункт меню: ",
    "invalid_choice": "Неверный выбор. Введите 'h' для справки.",
}

TASK1 = {
    "title": Messages.TASK1.title,
    "error_invalid_size": "Размер массива должен быть положительным числом",
    "error_empty_array": "Массив не может быть пустым",
    "error_length_mismatch": "Массивы должны быть одинаковой длины. Длина первого: {}, второго: {}",
    "error_invalid_numbers": "Введены некорректные числа",
    "error_array_too_large": "Сумма чисел слишком велика",
}

TASK4 = {
    "title": Messages.TASK4.title,
    "error_empty_input": "Ввод не может быть пустым",
    "error_invalid_digit": "Все цифры должны быть от 0 до 9",
    "error_invalid_operation": "Операция должна быть '+' или '-'",
    "error_negative_result": "Результат отрицательный: {}",
    "error_invalid_number": "Некорректные цифры для преобразования в число",
}

TASK5 = {
    "title": Messages.TASK5.title,
    "error_invalid_target": "Целевая сумма должна быть целым числом",
    "error_no_subarrays": "Не найдено подмассивов с заданной суммой",
    "subarray_found": "Найден подмассив с индексами [{}:{}]: {}",
}

HELP = {
    "title": "=== СПРАВКА ===",
    "task1": "1 - Обработка двух массивов (сортировка и поэлементное сложение)",
    "task4": "4 - Арифметические операции над числами в виде массивов",
    "task5": "5 - Поиск подмассивов с заданной суммой",
    "help": "h - Показать эту справку",
    "logging": "l - Изменить уровень логирования",
    "exit": "0 - Выйти из программы",
}