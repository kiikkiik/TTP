"""
ПОЛЬЗОВАТЕЛЬСКИЕ ИСКЛЮЧЕНИЯ С ДОПОЛНИТЕЛЬНОЙ ИНФОРМАЦИЕЙ

ОПТИМИЗАЦИИ:
1. Иерархия исключений для точной обработки
2. Контекстная информация в исключениях
3. Автоматическое логирование
4. Пользовательские сообщения об ошибках

ВАЖНОСТЬ:
1. Чистая обработка ошибок
2. Понятные сообщения пользователю
3. Упрощение отладки
4. Предотвращение падений бота
"""

from typing import Optional, Any, Dict
from logger import logger

class BotError(Exception):
    """
    Базовый класс всех исключений бота
    
    ДОПОЛНИТЕЛЬНЫЕ ВОЗМОЖНОСТИ:
    1. Автоматическое логирование
    2. Контекстная информация
    3. Пользовательские сообщения
    """
    
    def __init__(self, 
                 message: str, 
                 user_message: Optional[str] = None,
                 context: Optional[Dict[str, Any]] = None,
                 log_level: str = "ERROR"):
        """
        Инициализация исключения
        
        Args:
            message: внутреннее сообщение об ошибке (для логов)
            user_message: сообщение для показа пользователю
            context: дополнительный контекст ошибки
            log_level: уровень логирования (ERROR, WARNING, INFO)
        """
        self.message = message
        self.user_message = user_message or message
        self.context = context or {}
        self.log_level = log_level
        
        # Автоматическое логирование при создании исключения
        self._log_error()
        
        super().__init__(self.message)
    
    def _log_error(self):
        """Автоматическое логирование исключения"""
        log_message = f"{self.__class__.__name__}: {self.message}"
        
        if self.context:
            context_str = ", ".join(f"{k}={v}" for k, v in self.context.items())
            log_message += f" [Context: {context_str}]"
        
        # Используем глобальный логгер
        if self.log_level == "WARNING":
            logger.warning(log_message)
        elif self.log_level == "INFO":
            logger.info(log_message)
        else:
            logger.error(log_message)
    
    def to_dict(self) -> Dict[str, Any]:
        """Сериализация исключения в словарь (для API)"""
        return {
            "type": self.__class__.__name__,
            "message": self.message,
            "user_message": self.user_message,
            "context": self.context
        }

# ========== СПЕЦИАЛИЗИРОВАННЫЕ ИСКЛЮЧЕНИЯ ==========

class ValidationError(BotError):
    """
    Ошибка валидации входных данных
    
    Вызывается когда:
    1. Неправильный формат ввода
    2. Некорректные типы данных
    3. Нарушение ограничений (длина, диапазон)
    
    Пример использования:
        raise ValidationError(
            message="Массивы разной длины",
            user_message="Массивы должны быть одинаковой длины",
            context={"arr1_len": len(arr1), "arr2_len": len(arr2)}
        )
    """
    def __init__(self, message: str, user_message: Optional[str] = None, 
                 context: Optional[Dict[str, Any]] = None):
        super().__init__(message, user_message, context, log_level="WARNING")

class CalculationError(BotError):
    """
    Ошибка выполнения вычислений
    
    Вызывается когда:
    1. Математические ошибки (деление на 0)
    2. Переполнение вычислений
    3. Ошибки в алгоритмах
    
    Пример использования:
        raise CalculationError(
            message="Division by zero in calculation",
            user_message="Ошибка вычислений: деление на ноль",
            context={"operation": "division", "divisor": 0}
        )
    """
    def __init__(self, message: str, user_message: Optional[str] = None,
                 context: Optional[Dict[str, Any]] = None):
        super().__init__(message, user_message, context, log_level="ERROR")

class InputError(BotError):
    """
    Ошибка ввода пользователя
    
    Вызывается когда:
    1. Пользователь ввел некорректные данные
    2. Не хватает обязательных параметров
    3. Неподдерживаемый формат
    
    Пример использования:
        raise InputError(
            message="Invalid input format for task 1",
            user_message="Неверный формат. Используйте: 1 2 3;4 5 6",
            context={"input": user_input, "expected_format": "array;array"}
        )
    """
    def __init__(self, message: str, user_message: Optional[str] = None,
                 context: Optional[Dict[str, Any]] = None):
        super().__init__(message, user_message, context, log_level="INFO")

class ConfigurationError(BotError):
    """
    Ошибка конфигурации бота
    
    Вызывается когда:
    1. Неверный токен бота
    2. Отсутствуют обязательные настройки
    3. Ошибки в конфигурационных файлах
    """
    def __init__(self, message: str, user_message: Optional[str] = None,
                 context: Optional[Dict[str, Any]] = None):
        super().__init__(message, user_message or "Ошибка конфигурации бота", 
                        context, log_level="CRITICAL")

class ResourceError(BotError):
    """
    Ошибка ресурсов
    
    Вызывается когда:
    1. Закончилась память
    2. Превышены лимиты времени
    3. Проблемы с файловой системой
    """
    def __init__(self, message: str, user_message: Optional[str] = None,
                 context: Optional[Dict[str, Any]] = None):
        super().__init__(message, user_message or "Ошибка ресурсов", 
                        context, log_level="ERROR")

# ========== УТИЛИТЫ ДЛЯ РАБОТЫ С ИСКЛЮЧЕНИЯМИ ==========

def handle_bot_error(error: BotError) -> str:
    """
    Обработка исключения бота и возврат сообщения для пользователя
    
    Args:
        error: исключение BotError или его наследник
    
    Returns:
        str: сообщение для показа пользователю
    """
    return error.user_message

def safe_execute(func, *args, **kwargs):
    """
    Безопасное выполнение функции с перехватом исключений
    
    Args:
        func: функция для выполнения
        *args, **kwargs: аргументы функции
    
    Returns:
        tuple: (результат, ошибка_или_None)
    """
    try:
        result = func(*args, **kwargs)
        return result, None
    except BotError as e:
        return None, e
    except Exception as e:
        # Преобразование стандартных исключений в BotError
        bot_error = CalculationError(
            message=f"Unexpected error: {str(e)}",
            user_message="Внутренняя ошибка бота",
            context={"original_error": str(e), "function": func.__name__}
        )
        return None, bot_error