import json
from datetime import datetime
from decimal import Decimal
from pathlib import Path

from src.catalog import Catalog
from src.errors import DamagedFile, UnsupportedFormatVersion
from src.models import BookModel

RESULTS_DIR = Path(__file__).resolve().parent / "results"


class Storage:
    def __init__(self, version: int = 1):
        self.version: int = version
        self.counst_save: int = 1

    def save(self, catalog: Catalog) -> None:
        if not RESULTS_DIR.is_dir():
            RESULTS_DIR.mkdir()

        document = {"format_version": self.version, "data": {}}
        for book in catalog.data.values():
            timestamp = book.timestamp
            document["data"][book.id] = {
                "id": book.id,
                "title": book.title,
                "category": book.category,
                "author": book.author,
                "timestamp": (
                    timestamp.isoformat()
                    if isinstance(timestamp, datetime)
                    else timestamp
                ),
                "price": str(book.price),
            }
        with open(
            RESULTS_DIR / f"save_{self.counst_save}.json",
            mode="w",
            encoding="utf-8",
        ) as file:
            json.dump(document, file, indent=4)

        self.counst_save += 1

    def load(self, file: Path) -> list[BookModel]:
        document: dict | None = None
        with file.open(mode="r", encoding="utf-8") as f:
            try:
                document = json.load(f)
            except json.JSONDecodeError:
                raise DamagedFile(file_path=file)

        if document is None or not isinstance(document, dict):
            raise DamagedFile(file_path=file)

        if "format_version" not in document or "data" not in document:
            raise DamagedFile(file_path=file)

        format_version = document["format_version"]

        if not isinstance(format_version, int) or format_version != self.version:
            raise UnsupportedFormatVersion

        buffer_catalog: Catalog = Catalog()

        for book in document["data"].values():
            essence_book: BookModel = BookModel(
                id=book["id"],
                title=book["title"],
                category=book["category"],
                timestamp=(
                    datetime.fromisoformat(book["timestamp"])
                    if book["timestamp"]
                    else None
                ),
                author=book["author"],
                price=Decimal(book["price"]),
            )

            buffer_catalog.add(essence_book)

        return list(buffer_catalog.data.values())
