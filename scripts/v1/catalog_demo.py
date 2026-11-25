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
            id="4",
            title="Frankenstein",
            category="Fiction",
            timestamp=datetime(2026, 1, 4, 10, tzinfo=UTC),
            author="Mary Shelley",
            price=Decimal("10.50"),
        ),
        BookModel(
            id="5",
            title="The Time Machine",
            category="Science Fiction",
            timestamp=datetime(2026, 1, 5, 10, tzinfo=UTC),
            author="H. G. Wells",
            price=Decimal("9.75"),
        ),
        BookModel(
            id="6",
            title="On the Origin of Species",
            category="Science",
            timestamp="2026-01-02T00:00:00+00:00",
            author="Charles Darwin",
            price=Decimal("14.00"),
        ),
    )
    for book in books:
        catalog.add(book)

    catalog.load(file_path=Path("mocks/v1.json")) 

    catalog.remove("4")
    
    catalog.save(Path("save_v1.json"))
