"""
Главный модуль программы.
"""

import logging
import sys
from messages import COMMON, MENU, HELP, LOGGING
from task_1 import run_task1
from task_4 import run_task4
from task_5 import run_task5

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler("app.log", encoding='utf-8')]
)

logger = logging.getLogger(__name__)


def change_logging_level():
    """Изменение уровня логирования."""
    print(f"\n{LOGGING['title']}")
    print(LOGGING["levels"])
    print(LOGGING["level1"])
    print(LOGGING["level2"])
    print(LOGGING["level3"])
    print(LOGGING["level4"])
    print(LOGGING["level5"])
    
    choice = input(LOGGING["prompt_level"]).strip()
    
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
        
        # Обновляем уровень всех обработчиков
        for handler in logging.getLogger().handlers:
            handler.setLevel(new_level)
        
        level_name = logging.getLevelName(new_level)
        print(LOGGING["level_changed"].format(level_name))
        logger.info(LOGGING["level_changed"].format(level_name))
        
        # Демонстрация
        print(LOGGING["demo"].format(level_name))
        logger.debug("DEBUG сообщение")
        logger.info("INFO сообщение")
        logger.warning("WARNING сообщение")
        logger.error("ERROR сообщение")
        logger.critical("CRITICAL сообщение")
    else:
        logger.warning(LOGGING["invalid_level"])
        print(MENU["invalid_choice"])


def show_help():
    """Отображение справки."""
    print(f"\n{HELP['title']}")
    print(HELP["task1"])
    print(HELP["task4"])
    print(HELP["task5"])
    print(HELP["help"])
    print(HELP["logging"])
    print(HELP["exit"])
    logger.info("Показана справка")


def main_menu():
    """Главное меню программы."""
    logger.info(COMMON["program_start"])
    
    print("=" * 60)
    print("ПРОГРАММА ДЛЯ ВЫПОЛНЕНИЯ ЗАДАНИЙ ПО РАБОТЕ С МАССИВАМИ")
    print("=" * 60)
    
    menu_actions = {
        '1': {
            'name': MENU["task1"],
            'action': run_task1,
            'log': "Выбрано задание 1"
        },
        '4': {
            'name': MENU["task4"],
            'action': run_task4,
            'log': "Выбрано задание 4"
        },
        '5': {
            'name': MENU["task5"],
            'action': run_task5,
            'log': "Выбрано задание 5"
        },
        'h': {
            'name': MENU["help"],
            'action': show_help,
            'log': "Запрошена справка"
        },
        'l': {
            'name': MENU["logging"],
            'action': change_logging_level,
            'log': "Изменение уровня логирования"
        },
        '0': {
            'name': MENU["exit"],
            'action': lambda: None,
            'log': "Выход из программы"
        }
    }
    
    try:
        while True:
            print("\n" + "="*50)
            print(MENU["title"])
            
            # Динамическое отображение меню
            for key, value in menu_actions.items():
                print(f"{key}. {value['name']}")
            
            choice = input(MENU["prompt_choice"]).strip().lower()
            
            if choice == '0':
                logger.info(menu_actions['0']['log'])
                print(COMMON["program_exit"])
                break
            
            if choice in menu_actions:
                logger.info(menu_actions[choice]['log'])
                menu_actions[choice]['action']()
            else:
                logger.warning(f"Неверный выбор: '{choice}'")
                print(MENU["invalid_choice"])
                
    except (KeyboardInterrupt, EOFError):
        logger.info(COMMON["program_interrupted"])
        print(f"\n{COMMON['program_interrupted']}")
    except Exception as e:
        logger.critical(COMMON["unexpected_error"].format(e), exc_info=True)
        print(COMMON["unexpected_error"].format(e))
        print(COMMON["details_in_log"])


if __name__ == "__main__":
    main_menu()