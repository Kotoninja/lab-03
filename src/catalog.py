from src import errors
from src.models import BookModel


class Catalog:
    def __init__(self):
        self.data: dict[str, BookModel] = {}

    def add(self, item: BookModel) -> None:
        if item.id in self.data:
            raise errors.DuplicateID()
        self.data[item.id] = item

    def get(self, item_id: str) -> BookModel:
        if item_id not in self.data:
            raise errors.ObjectNotFound

        return self.data[item_id]

    def remove(self, item_id: str) -> None:
        if item_id not in self.data:
            raise errors.ObjectNotFound

        del self.data[item_id]

    def update(self, new_catalog: list[BookModel]) -> None:
        for obj in new_catalog:
            self.add(obj)

    def find_by_category(self, category: str) -> list[BookModel]:
        answer: list = []
        for book in self.data.values():
            if book.category == category:
                answer.append(book)

        if not answer:
            raise errors.ObjectNotFound
        return answer

    def find_by_name(self, query: str) -> BookModel:
        for book in self.data.values():
            if book.title.casefold() == query.casefold():
                return book
        raise errors.ObjectNotFound

    def __len__(self) -> int:
        return len(self.data)

    def __iter__(self):
        """Итерации идут в порядке добавления кинг"""
        return iter(self.data.values())

    def __contains__(self, item_id):
        return item_id in self.data
