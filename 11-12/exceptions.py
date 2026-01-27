"""
exceptions.py

Содержит классы исключений для приложения.
"""

class AppException(Exception):
    """Базовый класс всех исключений приложения"""
    pass

class InvalidInputError(AppException):
    """Ошибка некорректного пользовательского ввода"""
    pass

class InvalidArrayError(AppException):
    """Ошибка при вводе недопустимого массива"""
    pass

class InvalidNumberError(AppException):
    """Ошибка при вводе недопустимого числа"""
    pass

class UnsupportedOperationError(AppException):
    """Операция не поддерживается"""
    pass

class ArrayLengthMismatchError(AppException):
    """Длины массивов не совпадают"""
    pass

class EmptyArrayError(AppException):
    """Массив пуст"""
    pass

class NegativeResultError(AppException):
    """Результат отрицателен и не поддерживается"""
    pass

class ValidationError(AppException):
    """Ошибка валидации данных"""
    pass

class CalculationError(AppException):
    """Ошибка при вычислениях"""
    pass

# Дополнительные исключения для совместимости
class AppError(AppException):
    """Алиас для совместимости"""
    pass

class DataNotSetError(AppException):
    """Данные не заданы"""
    pass

class OperationError(AppException):
    """Ошибка выполнения операции"""
    pass

class InvalidValueError(AppException):
    """Некорректные значения"""
    pass