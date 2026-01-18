"""
Модуль с пользовательскими исключениями для программы работы с массивами.
"""

class AppException(Exception):
    """Базовое исключение приложения"""
    pass


class InvalidInputError(AppException):
    """Ошибка некорректного пользовательского ввода"""
    pass


class InvalidArrayError(InvalidInputError):
    """Ошибка при вводе недопустимого массива"""
    pass


class InvalidNumberError(InvalidInputError):
    """Ошибка при вводе недопустимого числа"""
    pass


class UnsupportedOperationError(AppException):
    """Операция не поддерживается"""
    pass


class ArrayLengthMismatchError(AppException):
    """Длины массивов не совпадают"""
    pass


class EmptyArrayError(InvalidArrayError):
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