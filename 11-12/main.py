"""
Главный модуль приложения (корутинный FSM)
"""

import logging
from messages import MESSAGES
from task_1 import task1_fsm
from task_4 import task4_fsm
from task_5 import task5_fsm

logger = logging.getLogger(__name__)
msgs = MESSAGES["main_menu"]

def show_help():
    """Показывает справку."""
    print("\n=== СПРАВКА ===")
    print("1 - Обработка двух массивов (сортировка и поэлементное сложение)")
    print("4 - Арифметические операции над числами в виде массивов")
    print("5 - Поиск подмассивов с заданной суммой")
    print("h - Показать эту справку")
    print("l - Изменить уровень логирования")
    print("0 - Выйти из программы")
    logger.info("Показана справка")

def change_logging_level():
    """Изменяет уровень логирования."""
    print("\n=== Изменение уровня логирования ===")
    print("Доступные уровни:")
    print("1. DEBUG - все сообщения")
    print("2. INFO - информационные сообщения")
    print("3. WARNING - только предупреждения")
    print("4. ERROR - только ошибки")
    print("5. CRITICAL - только критические ошибки")
    
    choice = input("Выберите уровень (1-5): ").strip()
    
    level_map = {
        '1': logging.DEBUG,
        '2': logging.INFO,
        '3': logging.WARNING,
        '4': logging.ERROR,
        '5': logging.CRITICAL
    }
    
    if choice in level_map:
        new_level = level_map[choice]
        logging.getLogger().setLevel(new_level)
        level_name = logging.getLevelName(new_level)
        print(f"Уровень логирования изменен на: {level_name}")
        logger.info(f"Уровень логирования изменен на: {level_name}")
    else:
        print("Неверный выбор уровня")
        logger.warning("Неверный выбор уровня логирования")


def main_fsm():
    """
    Корутина главного меню верхнего уровня.
    """
    while True:
        print("\n" + msgs["title"])
        for option in msgs["options"]:
            print(option)

        choice = yield
        logger.info(f"MAIN choice: {choice}")

        try:
            if choice == "1":
                fsm = task1_fsm()
                next(fsm)
                while True:
                    try:
                        sub_choice = input(msgs["prompt"]).strip()
                        fsm.send(sub_choice)
                    except StopIteration:
                        break
                        
            elif choice == "4":
                fsm = task4_fsm()
                next(fsm)
                while True:
                    try:
                        sub_choice = input(msgs["prompt"]).strip()
                        fsm.send(sub_choice)
                    except StopIteration:
                        break
                        
            elif choice == "5":
                fsm = task5_fsm()
                next(fsm)
                while True:
                    try:
                        sub_choice = input(msgs["prompt"]).strip()
                        fsm.send(sub_choice)
                    except StopIteration:
                        break
                        
            elif choice == "h":
                show_help()
            elif choice == "l":
                change_logging_level()
            elif choice == "0":
                print(msgs["exit"])
                logger.info("Application exit")
                return
            else:
                print(msgs["invalid"])

        except Exception as e:
            print(f"Ошибка: {e}")
            logger.error(f"Error: {e}")

def main():
    # Настройка логирования
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.FileHandler("app.log", encoding='utf-8')]
    )
    
    logger.info("Программа запущена")
    print("=" * 60)
    print("ПРОГРАММА ДЛЯ ВЫПОЛНЕНИЯ ЗАДАНИЙ ПО РАБОТЕ С МАССИВАМИ")
    print("=" * 60)

    fsm = main_fsm()
    next(fsm)
    
    while True:
        try:
            choice = input(msgs["prompt"]).strip().lower()
            fsm.send(choice)
        except StopIteration:
            break
        except KeyboardInterrupt:
            print("\n\nПрограмма прервана пользователем")
            break
        except Exception as e:
            print(f"Неожиданная ошибка: {e}")
            logger.exception(f"Unhandled exception: {e}")

if __name__ == "__main__":
    main()