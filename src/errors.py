from pathlib import Path


class CatalogError(Exception):
    """Базовое исключение"""


class InvalidEssence(CatalogError):
    """Неверная сущность"""
    def __init__(self, text) -> None:
        if text:
            super().__init__(f"Неверная сущность: {text}")
        else:
            super().__init__("Неверная сущность")


class DuplicateID(CatalogError):
    def __init__(self) -> None:
        super().__init__("Дубликат ID")


class ObjectNotFound(CatalogError):
    def __init__(self) -> None:
        super().__init__("Объект не найден")


class UnsupportedFormatVersion(CatalogError):
    def __init__(self) -> None:
        super().__init__("Неподдерживаемая версия формата")


class DamagedFile(CatalogError):
    """Повреждённый файл."""
    def __init__(self, file_path: Path) -> None:
        if file_path:
            super().__init__(f"Поврежденный файл: {file_path}")
        else:
            super().__init__("Поврежденный файл")
