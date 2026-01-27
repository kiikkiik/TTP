import asyncio
import random
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.storage.memory import MemoryStorage

# ========== КОНФИГУРАЦИЯ БОТА ==========

TOKEN = "8525462952:AAFx6PjQFg08wK5FpMsknLcbO0FebBhyTzc"

# ИНИЦИАЛИЗАЦИЯ КОМПОНЕНТОВ AIOGRAM:
# 1. Bot - основной объект для работы с Telegram API
# 2. Dispatcher - маршрутизатор сообщений
# 3. MemoryStorage - хранилище состояний в оперативной памяти
bot = Bot(token=TOKEN)  # Создаем экземпляр бота
dp = Dispatcher(storage=MemoryStorage())  # Создаем диспетчер с хранилищем в памяти

# СЛОВАРЬ ДЛЯ ХРАНЕНИЯ СОСТОЯНИЙ ПОЛЬЗОВАТЕЛЕЙ
# Ключ: user_id (уникальный ID пользователя в Telegram)
# Значение: словарь с состоянием и данными пользователя
users = {}

# ========== ИМПОРТ ВНЕШНИХ МОДУЛЕЙ ==========

from logger import log  # Функции логгирования
from exceptions import *  # Пользовательские исключения
from messages import *  # Текстовые сообщения
from task_1 import execute_1  # Алгоритм задания 1
from task_4 import execute_4  # Алгоритм задания 4
from task_5 import execute_5  # Алгоритм задания 5

# ========== КЛАВИАТУРЫ (КНОПКИ) ==========

def get_kb(buttons):
    """
    Создает клавиатуру с кнопками
    Parameters:
        buttons: список строк - тексты кнопок
    Returns:
        ReplyKeyboardMarkup - объект клавиатуры
    """
    # Создаем массив кнопок: каждая кнопка в отдельном ряду
    keyboard = [[KeyboardButton(text=b)] for b in buttons]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# ГЛАВНОЕ МЕНЮ - 4 кнопки выбора задания + помощь
MAIN_KB = get_kb(["Задание 1", "Задание 4", "Задание 5", "Помощь"])

# МЕНЮ ЗАДАНИЯ - общие действия для всех заданий
TASK_KB = get_kb(["Ввести", "Сгенерировать", "Выполнить", "Результат", "Назад"])

# ========== ОБРАБОТЧИКИ КОМАНД ==========

@dp.message(F.text == "/start")
async def start_cmd(msg: Message):
    """
    Обработчик команды /start
    Вызывается когда пользователь пишет /start или первый раз пишет боту
    """
    user_id = msg.from_user.id  # Получаем уникальный ID пользователя
    
    # Инициализируем состояние пользователя в словаре users
    # "state": "main" - пользователь в главном меню
    # Позже добавим другие состояния: "task1", "task4", "task5", "await_op"
    users[user_id] = {"state": "main"}
    
    # Отправляем приветственное сообщение с главной клавиатурой
    await msg.answer(WELCOME, reply_markup=MAIN_KB)
    
    # Логируем событие
    log(f"User {user_id} started")

@dp.message(F.text == "Помощь")
async def help_cmd(msg: Message):
    """
    Обработчик кнопки "Помощь"
    Показывает справку по использованию бота
    """
    await msg.answer(HELP_TEXT)

@dp.message(F.text == "Назад")
async def back_cmd(msg: Message):
    """
    Обработчик кнопки "Назад"
    Возвращает пользователя в главное меню
    """
    user_id = msg.from_user.id
    
    # Сбрасываем состояние на "main" (главное меню)
    users[user_id] = {"state": "main"}
    
    # Показываем главное меню
    await msg.answer("Главное меню:", reply_markup=MAIN_KB)

@dp.message(F.text.startswith("Задание"))
async def task_select(msg: Message):
    """
    Обработчик выбора задания (кнопки "Задание 1", "Задание 4", "Задание 5")
    """
    user_id = msg.from_user.id
    
    # Извлекаем номер задания из текста: "Задание 1" → "1"
    task_num = msg.text.split()[1]
    
    # Устанавливаем состояние пользователя:
    # "state": "task1"/"task4"/"task5" - указывает, какое задание выбрано
    # "task": "1"/"4"/"5" - номер задания (сохраняем отдельно для удобства)
    # "data": {} - пустой словарь для хранения введенных данных
    users[user_id] = {
        "state": f"task{task_num}",
        "task": task_num,
        "data": {}
    }
    
    # Показываем описание выбранного задания и меню действий
    await msg.answer(TASK_DESC[task_num], reply_markup=TASK_KB)

@dp.message(F.text == "Сгенерировать")
async def generate_data(msg: Message):
    """
    Обработчик кнопки "Сгенерировать"
    Генерирует случайные данные для выбранного задания
    """
    user_id = msg.from_user.id
    user = users.get(user_id, {})  # Получаем данные пользователя
    task = user.get("task", "1")  # Получаем номер задания (по умолчанию 1)
    
    # ГЕНЕРАЦИЯ ДЛЯ ЗАДАНИЯ 1
    if task == "1":
        # Генерируем 2 массива по 5 случайных чисел от -10 до 10
        arr1 = [random.randint(-10, 10) for _ in range(5)]
        arr2 = [random.randint(-10, 10) for _ in range(5)]
        
        # Сохраняем сгенерированные данные
        users[user_id]["data"] = {"arr1": arr1, "arr2": arr2}
        
        # Показываем пользователю что сгенерировали
        await msg.answer(f"Сгенерировано:\nМассив1: {arr1}\nМассив2: {arr2}")
    
    # ГЕНЕРАЦИЯ ДЛЯ ЗАДАНИЯ 4
    elif task == "4":
        # Генерируем два трехзначных числа
        num1 = random.randint(100, 999)
        num2 = random.randint(100, 999)
        
        # Преобразуем числа в массивы цифр: 123 → [1, 2, 3]
        arr1 = [int(d) for d in str(num1)]
        arr2 = [int(d) for d in str(num2)]
        
        # Сохраняем данные
        users[user_id]["data"] = {"arr1": arr1, "arr2": arr2}
        
        await msg.answer(f"Сгенерировано:\nЧисло1: {arr1}\nЧисло2: {arr2}")
    
    # ГЕНЕРАЦИЯ ДЛЯ ЗАДАНИЯ 5
    elif task == "5":
        # Генерируем массив из 8 чисел и целевую сумму
        arr = [random.randint(-5, 10) for _ in range(8)]
        target = random.randint(0, 20)
        
        # Сохраняем данные
        users[user_id]["data"] = {"arr": arr, "target": target}
        
        await msg.answer(f"Сгенерировано:\nМассив: {arr}\nСумма: {target}")
    
    # Логируем событие
    log(f"User {user_id} generated data for task {task}")

@dp.message(F.text == "Выполнить")
async def execute_task(msg: Message):
    """
    Обработчик кнопки "Выполнить"
    Запускает расчет для выбранного задания
    """
    user_id = msg.from_user.id
    user = users.get(user_id, {})  # Данные пользователя
    data = user.get("data", {})  # Введенные/сгенерированные данные
    task = user.get("task", "1")  # Номер задания
    
    try:
        # ВЫПОЛНЕНИЕ ЗАДАНИЯ 1
        if task == "1" and "arr1" in data and "arr2" in data:
            # Вызываем алгоритм из task_1.py
            result = execute_1(data["arr1"], data["arr2"])
            
            # Сохраняем результат
            users[user_id]["result"] = result
            
            await msg.answer(f"Результат вычислен: {result}")
        
        # ВЫПОЛНЕНИЕ ЗАДАНИЯ 4
        elif task == "4" and "arr1" in data and "arr2" in data:
            # Проверяем, выбрана ли операция
            if "operation" not in data:
                await msg.answer("Введите операцию (+ или -):")
                
                # Меняем состояние - ждем ввода операции
                users[user_id]["state"] = "await_op"
                return
            
            # Вызываем алгоритм из task_4.py
            result = execute_4(data["arr1"], data["arr2"], data["operation"])
            
            # Сохраняем результат
            users[user_id]["result"] = result
            
            await msg.answer(f"Результат вычислен: {result}")
        
        # ВЫПОЛНЕНИЕ ЗАДАНИЯ 5
        elif task == "5" and "arr" in data and "target" in data:
            # Вызываем алгоритм из task_5.py
            result = execute_5(data["arr"], data["target"])
            
            # Сохраняем результат
            users[user_id]["result"] = result
            
            await msg.answer(f"Найдено подмассивов: {result}")
        
        # ЕСЛИ ДАННЫХ НЕТ
        else:
            await msg.answer("Сначала введите или сгенерируйте данные!")
    
    except Exception as e:
        # Обрабатываем ошибки (исключения из task_*.py)
        await msg.answer(f"Ошибка: {e}")
        
        # Логируем ошибку
        log(f"Error in task {task}: {e}")

@dp.message(F.text == "Результат")
async def show_result(msg: Message):
    """
    Обработчик кнопки "Результат"
    Показывает последний сохраненный результат
    """
    user_id = msg.from_user.id
    result = users.get(user_id, {}).get("result")  # Получаем результат
    
    # Если результат есть - показываем, иначе просим выполнить расчет
    if result:
        await msg.answer(f"Результат: {result}")
    else:
        await msg.answer("Сначала выполните расчет!")

# ========== ОБРАБОТЧИК ТЕКСТОВОГО ВВОДА ==========

@dp.message()
async def handle_text(msg: Message):
    """
    Обработчик ВСЕХ текстовых сообщений, не обработанных другими обработчиками
    Здесь обрабатываем ручной ввод данных
    """
    user_id = msg.from_user.id
    user = users.get(user_id, {})  # Получаем данные пользователя
    state = user.get("state", "")  # Текущее состояние
    text = msg.text.strip()  # Текст сообщения (убираем пробелы)
    
    # ВВОД ДАННЫХ ДЛЯ ЗАДАНИЯ 1
    # Формат: "1 2 3;4 5 6"
    if state == "task1" and user.get("task") == "1":
        try:
            # Разделяем на две части по ";"
            # arr1_text = "1 2 3", arr2_text = "4 5 6"
            arr1_text, arr2_text = map(lambda x: x.strip(), text.split(";"))
            
            # Преобразуем строки в списки чисел
            # "1 2 3" → [1, 2, 3]
            arr1 = list(map(int, arr1_text.split()))
            arr2 = list(map(int, arr2_text.split()))
            
            # Сохраняем данные
            users[user_id]["data"] = {"arr1": arr1, "arr2": arr2}
            
            # Подтверждаем сохранение
            await msg.answer(f"Сохранено:\nМассив1: {arr1}\nМассив2: {arr2}")
        
        except:
            # Если ошибка формата - показываем пример
            await msg.answer("Ошибка формата! Используйте: '1 2 3;4 5 6'")
    
    # ВВОД ДАННЫХ ДЛЯ ЗАДАНИЯ 4
    # Два формата:
    # 1. Полный: "1 2 3|4 5 6;+" (числа и операция сразу)
    # 2. Поэтапный: сначала числа, потом операция
    elif state == "task4" and user.get("task") == "4":
        # ПОЛНЫЙ ФОРМАТ (числа + операция)
        if ";" in text:
            try:
                # Разделяем: nums="1 2 3|4 5 6", op="+"
                nums, op = text.split(";")
                
                # Разделяем числа: left="1 2 3", right="4 5 6"
                arr1_text, arr2_text = map(lambda x: x.strip(), nums.split("|"))
                
                # Преобразуем в списки чисел
                arr1 = list(map(int, arr1_text.split()))
                arr2 = list(map(int, arr2_text.split()))
                
                # Сохраняем все данные
                users[user_id]["data"] = {"arr1": arr1, "arr2": arr2, "operation": op}
                
                await msg.answer(f"Сохранено:\nЧисло1: {arr1}\nЧисло2: {arr2}\nОперация: {op}")
            
            except:
                await msg.answer("Ошибка! Формат: '1 2 3|4 5 6;+'")
        
        # ТОЛЬКО ОПЕРАЦИЯ (если числа уже введены)
        elif text in "+-":
            # Добавляем операцию к существующим данным
            users[user_id]["data"]["operation"] = text
            
            await msg.answer(f"Операция сохранена: {text}")
    
    # ВВОД ДАННЫХ ДЛЯ ЗАДАНИЯ 5
    # Формат: "1 2 3 4;5"
    elif state == "task5" and user.get("task") == "5":
        try:
            # Разделяем: arr_text="1 2 3 4", target_text="5"
            arr_text, target_text = text.split(";")
            
            # Преобразуем
            arr = list(map(int, arr_text.split()))  # "1 2 3 4" → [1, 2, 3, 4]
            target = int(target_text.strip())  # "5" → 5
            
            # Сохраняем
            users[user_id]["data"] = {"arr": arr, "target": target}
            
            await msg.answer(f"Сохранено:\nМассив: {arr}\nСумма: {target}")
        
        except:
            await msg.answer("Ошибка! Формат: '1 2 3 4;5'")
    
    # ОЖИДАНИЕ ОПЕРАЦИИ ДЛЯ ЗАДАНИЯ 4
    elif state == "await_op" and text in "+-":
        # Пользователь ввел операцию после запроса
        users[user_id]["data"]["operation"] = text
        users[user_id]["state"] = "task4"  # Возвращаем в обычное состояние
        
        await msg.answer(f"Операция сохранена: {text}")
    
    # НЕИЗВЕСТНАЯ КОМАНДА
    else:
        await msg.answer("Используйте кнопки меню")

# ========== ФУНКЦИЯ ЗАПУСКА ==========

async def run():
    """
    Основная функция запуска бота
    Вызывается из main.py
    """
    print("Бот запущен. Используйте /start в Telegram")
    
    # Запускаем "опрос" (polling) - бот постоянно проверяет новые сообщения
    # Это основной цикл работы бота
    await dp.start_polling(bot)