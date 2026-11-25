from pathlib import Path

from src import errors, repository
from src.models import BookModel


class Catalog:
    """Каталог объектов"""

    def __init__(self):
        """Инитиализация каталога"""
        self.data: dict[str, BookModel] = {}

    def add(self, item: BookModel) -> None:
        """Добавление в каталог"""
        if not isinstance(item, BookModel):
            raise errors.InvalidEssence
        if item.id in self.data:
            raise errors.DuplicateID
        self.data[item.id] = item

    def get(self, item_id: str) -> BookModel:
        """Получить объект из каталога"""
        if item_id not in self.data:
            raise errors.ObjectNotFound

        return self.data[item_id]

    def remove(self, item_id: str) -> None:
        """Удалить объект из каталога"""
        if item_id not in self.data:
            raise errors.ObjectNotFound

        del self.data[item_id]

    def update(self, new_catalog: list[BookModel]) -> None:
        """Синхронизировать список объектов с каталогом"""

        for obj in new_catalog:
            if obj.id in self:
                raise errors.DuplicateID

        for obj in new_catalog:
            self.add(obj)

    def find_by_category(self, category: str) -> list[BookModel]:
        """Найти объект по категории"""
        answer: list = []
        for book in self.data.values():
            if book.category == category:
                answer.append(book)

        if not answer:
            raise errors.ObjectNotFound
        return answer

    def find_by_name(self, query: str) -> BookModel:
        """Найти объект по имени"""
        for book in self.data.values():
            if book.title.casefold() == query.casefold():
                return book
        raise errors.ObjectNotFound

    def save(self, file_path: Path):
        """Сохранить каталог в JSON"""
        repository.save(file_path=file_path, catalog=self)

    def load(self, file_path: Path):
        """Загрузить каталог из JSON"""
        self.update(repository.load(file_path=file_path))

    def __len__(self) -> int:
        """Получить длину каталога (сколько всего объектов в каталоге)"""
        return len(self.data)

    def __iter__(self):
        """Итерации идут в порядке добавления кинг"""
        return iter(self.data.values())

    def __contains__(self, item_id):
        """Если ли объект в каталоге"""
        return item_id in self.data
