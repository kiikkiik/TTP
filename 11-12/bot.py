"""
Основной модуль бота
"""

import asyncio
import random
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.storage.memory import MemoryStorage

# ========== КОНФИГУРАЦИЯ ==========
TOKEN = "8525462952:AAFx6PjQFg08wK5FpMsknLcbO0FebBhyTzc"

# Сначала создаем объекты
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Потом импортируем модули
from logger import log
# Импортируем конкретные переменные из messages
from messages import WELCOME, HELP, TASK1_DETAILS, TASK4_DETAILS, TASK5_DETAILS
from task_1 import execute_1
from task_4 import execute_4
from task_5 import execute_5

# ========== КЛАВИАТУРЫ ==========
def get_kb(buttons):
    """Создает клавиатуру"""
    kb = [[KeyboardButton(text=b)] for b in buttons]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

MAIN_KB = get_kb(["Задание 1", "Задание 4", "Задание 5", "Помощь"])
TASK_KB = get_kb(["Ввести", "Сгенерировать", "Выполнить", "Результат", "Назад"])

# ========== ХРАНИЛИЩЕ ПОЛЬЗОВАТЕЛЕЙ ==========
users = {}

# ========== ОБРАБОТЧИКИ ==========

@dp.message(F.text == "/start")
async def start_cmd(msg: Message):
    """Обработчик /start"""
    users[msg.from_user.id] = {"state": "main"}
    await msg.answer(WELCOME, reply_markup=MAIN_KB)
    log(f"User {msg.from_user.id} started")

@dp.message(F.text == "Помощь")
async def help_cmd(msg: Message):
    """Обработчик помощи"""
    await msg.answer(HELP)

@dp.message(F.text == "Назад")
async def back_cmd(msg: Message):
    """Возврат в главное меню"""
    users[msg.from_user.id] = {"state": "main"}
    await msg.answer("Главное меню:", reply_markup=MAIN_KB)

@dp.message(F.text.startswith("Задание"))
async def task_select(msg: Message):
    """Выбор задания"""
    uid = msg.from_user.id
    task_num = msg.text.split()[1]
    users[uid] = {
        "state": f"task{task_num}",
        "task": task_num,
        "data": {}
    }
    
    # Используем правильную переменную для описания задания
    if task_num == "1":
        task_desc = TASK1_DETAILS
    elif task_num == "4":
        task_desc = TASK4_DETAILS
    elif task_num == "5":
        task_desc = TASK5_DETAILS
    else:
        task_desc = f"Задание {task_num}"
    
    await msg.answer(f"Задание {task_num}:\n{task_desc}", reply_markup=TASK_KB)

@dp.message(F.text == "Сгенерировать")
async def generate_data(msg: Message):
    """Генерация данных"""
    uid = msg.from_user.id
    user = users.get(uid, {})
    task = user.get("task", "1")
    
    if task == "1":
        arr1 = [random.randint(-10, 10) for _ in range(5)]
        arr2 = [random.randint(-10, 10) for _ in range(5)]
        users[uid]["data"] = {"arr1": arr1, "arr2": arr2}
        await msg.answer(f"Сгенерировано:\nМассив1: {arr1}\nМассив2: {arr2}")
    
    elif task == "4":
        num1 = random.randint(100, 999)
        num2 = random.randint(100, 999)
        arr1 = [int(d) for d in str(num1)]
        arr2 = [int(d) for d in str(num2)]
        users[uid]["data"] = {"arr1": arr1, "arr2": arr2}
        await msg.answer(f"Сгенерировано:\nЧисло1: {arr1}\nЧисло2: {arr2}")
    
    elif task == "5":
        arr = [random.randint(-5, 10) for _ in range(8)]
        target = random.randint(0, 20)
        users[uid]["data"] = {"arr": arr, "target": target}
        await msg.answer(f"Сгенерировано:\nМассив: {arr}\nСумма: {target}")
    
    log(f"User {uid} generated data for task {task}")

@dp.message(F.text == "Выполнить")
async def execute_task(msg: Message):
    """Выполнение расчета"""
    uid = msg.from_user.id
    user = users.get(uid, {})
    data = user.get("data", {})
    task = user.get("task", "1")
    
    try:
        if task == "1" and "arr1" in data and "arr2" in data:
            result = execute_1(data["arr1"], data["arr2"])
            users[uid]["result"] = result
            await msg.answer(f"Результат: {result}")
        
        elif task == "4" and "arr1" in data and "arr2" in data:
            if "operation" not in data:
                await msg.answer("Введите операцию (+ или -):")
                users[uid]["state"] = "await_op"
                return
            result = execute_4(data["arr1"], data["arr2"], data["operation"])
            users[uid]["result"] = result
            await msg.answer(f"Результат: {result}")
        
        elif task == "5" and "arr" in data and "target" in data:
            result = execute_5(data["arr"], data["target"])
            users[uid]["result"] = result
            await msg.answer(f"Найдено подмассивов: {result}")
        
        else:
            await msg.answer("Сначала введите или сгенерируйте данные!")
    
    except Exception as e:
        await msg.answer(f"Ошибка: {e}")
        log(f"Error in task {task}: {e}")

@dp.message(F.text == "Результат")
async def show_result(msg: Message):
    """Показ результата"""
    uid = msg.from_user.id
    result = users.get(uid, {}).get("result")
    await msg.answer(f"Результат: {result}" if result else "Сначала выполните расчет!")

@dp.message()
async def handle_text(msg: Message):
    """Обработка текстового ввода"""
    uid = msg.from_user.id
    user = users.get(uid, {})
    state = user.get("state", "")
    text = msg.text.strip()
    
    if state == "task1" and user.get("task") == "1":
        try:
            arr1, arr2 = map(lambda x: list(map(int, x.split())), text.split(";"))
            users[uid]["data"] = {"arr1": arr1, "arr2": arr2}
            await msg.answer(f"Сохранено:\nМассив1: {arr1}\nМассив2: {arr2}")
        except:
            await msg.answer("Формат: '1 2 3;4 5 6'")
    
    elif state == "task4" and user.get("task") == "4":
        if ";" in text:
            try:
                nums, op = text.split(";")
                arr1, arr2 = map(lambda x: list(map(int, x.split())), nums.split("|"))
                users[uid]["data"] = {"arr1": arr1, "arr2": arr2, "operation": op}
                await msg.answer(f"Сохранено:\nЧисло1: {arr1}\nЧисло2: {arr2}\nОперация: {op}")
            except:
                await msg.answer("Формат: '1 2 3|4 5 6;+'")
        elif text in "+-":
            users[uid]["data"]["operation"] = text
            await msg.answer(f"Операция сохранена: {text}")
    
    elif state == "task5" and user.get("task") == "5":
        try:
            arr_text, target_text = text.split(";")
            arr = list(map(int, arr_text.split()))
            target = int(target_text)
            users[uid]["data"] = {"arr": arr, "target": target}
            await msg.answer(f"Сохранено:\nМассив: {arr}\nСумма: {target}")
        except:
            await msg.answer("Формат: '1 2 3 4;5'")
    
    elif state == "await_op" and text in "+-":
        users[uid]["data"]["operation"] = text
        users[uid]["state"] = "task4"
        await msg.answer(f"Операция сохранена: {text}")
    
    else:
        await msg.answer("Используйте кнопки меню")

# ========== ЗАПУСК ==========
async def main():
    """Главная функция запуска"""
    print("Бот запущен. Используйте /start в Telegram")
    await dp.start_polling(bot)