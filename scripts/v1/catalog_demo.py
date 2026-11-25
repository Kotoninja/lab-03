from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path

from src.catalog import Catalog
from src.models import BookModel

SOURCE_DIR = Path(__file__).resolve().parents[2] / "src"


def run() -> None:
    catalog = Catalog()

    books = (
        BookModel(
            id="book-1",
            title="Frankenstein",
            category="Fiction",
            timestamp=datetime(2026, 1, 4, 10, tzinfo=UTC),
            author="Mary Shelley",
            price=Decimal("15.2"),
        ),
    )
    for book in books:
        catalog.add(book)

    print(catalog.data)
    catalog.load(file_path=Path("mocks/v1.json")) 
    print(catalog.data)
    # catalog.save(Path("save_v1.json"))
