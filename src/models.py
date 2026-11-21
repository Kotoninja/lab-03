from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from src import errors


@dataclass
class BookModel:
    id: str
    title: str
    category: str
    timestamp: datetime | None | str
    author: str
    price: Decimal

    def __post_init__(self):
        if not isinstance(self.id, str) or not self.id:
            raise errors.InvalidEssence("Поле id должно быть непустой строкой")
        elif not isinstance(self.title, str) or not self.title.strip():
            raise errors.InvalidEssence("Поле title должно быть непустой строкой")
        elif not isinstance(self.category, str) or not self.category.strip():
            raise errors.InvalidEssence("Поле category должно быть непустой строкой")
        elif not isinstance(self.author, str) or not self.author.strip():
            raise errors.InvalidEssence("Поле author должно быть непустой строкой")
        elif not isinstance(self.price, Decimal) or not self.price:
            raise errors.InvalidEssence("Поле price должно быть ненулевым числом")
        elif not self.timestamp or (
            isinstance(self.timestamp, str) and not self.timestamp
        ):
            raise errors.InvalidEssence("Поле timestamp должно быть непустым полем")

        try:
            self.timestamp = datetime.fromisoformat(str(self.timestamp))
        except (ValueError, TypeError, AttributeError):
            raise errors.InvalidEssence("У поля timestamp неверная временная метка")
