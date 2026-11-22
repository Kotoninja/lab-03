from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from src import errors


@dataclass
class BookModel:
    id: str
    title: str
    category: str
    timestamp: datetime | str | None
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
            isinstance(self.timestamp, str) and not self.timestamp.strip()
        ):
            raise errors.InvalidEssence("Поле timestamp должно быть непустым полем")

        try:
            self.timestamp = datetime.fromisoformat(str(self.timestamp))
            if self.timestamp.tzinfo is None:
                raise errors.InvalidEssence("Поле timestamp должно содержать дату и время с указанием часового пояса.")
        except (ValueError, TypeError, AttributeError):
            raise errors.InvalidEssence("У поля timestamp неверная временная метка")
