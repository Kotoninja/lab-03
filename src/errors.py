from pathlib import Path


class CatalogError(BaseException): ...


class InvalidEssence(CatalogError):
    def __init__(self, text) -> None:
        if text:
            super().__init__(f"Неверная сущность: {text}\n")
        else:
            super().__init__("Неверная сущность\n")


class DuplicateID(CatalogError):
    def __init__(self) -> None:
        super().__init__("Дубликат ID\n")


class ObjectNotFound(CatalogError):
    def __init__(self) -> None:
        super().__init__("Объект не найден\n")


class UnsupportedFormatVersion(CatalogError):
    def __init__(self) -> None:
        super().__init__("Неподдерживаемая версия формата\n")


class DamagedFile(CatalogError):
    def __init__(self, file_path: Path) -> None:
        if file_path:
            super().__init__(f"Поврежденный файл: {file_path}\n")
        else:
            super().__init__("Поврежденный файл\n")
