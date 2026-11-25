from __future__ import annotations

import json
from datetime import datetime
from decimal import Decimal
from pathlib import Path

from src.constans import FORMAT_VERSION, LOAD_DIR, RESULTS_DIR
from src.errors import DamagedFile, UnsupportedFormatVersion
from src.models import BookModel


def save(file_path: Path, catalog):
    """Сохранить каталог в JSON"""
    if not RESULTS_DIR.is_dir():
        RESULTS_DIR.mkdir()

    books: dict[str, dict[str, str | None]] = {}
    for book in catalog.data.values():
        timestamp = book.timestamp
        books[book.id] = {
            "id": book.id,
            "title": book.title,
            "category": book.category,
            "author": book.author,
            "timestamp": (
                timestamp.isoformat() if isinstance(timestamp, datetime) else timestamp
            ),
            "price": str(book.price),
        }
    with open(
        RESULTS_DIR / file_path,
        mode="w",
        encoding="utf-8",
    ) as file:
        json.dump({"format_version": FORMAT_VERSION, "data": books}, file, indent=4)


def load(file_path: Path) -> list[BookModel]:
    from src.catalog import Catalog

    """Загрузить каталог из JSON"""

    document: dict | None = None
    with open(LOAD_DIR / file_path, mode="r", encoding="utf-8") as f:
        try:
            document = json.load(f)
        except json.JSONDecodeError:
            raise DamagedFile(file_path=file_path)

    if document is None or not isinstance(document, dict):
        raise DamagedFile(file_path=file_path)

    if "format_version" not in document or "data" not in document:
        raise DamagedFile(file_path=file_path)

    format_version = document["format_version"]

    if not isinstance(format_version, int) or format_version != FORMAT_VERSION:
        raise UnsupportedFormatVersion

    buffer_catalog: Catalog = Catalog()

    for book in document["data"].values():
        essence_book: BookModel = BookModel(
            id=book["id"],
            title=book["title"],
            category=book["category"],
            timestamp=(
                datetime.fromisoformat(book["timestamp"]) if book["timestamp"] else None
            ),
            author=book["author"],
            price=Decimal(book["price"]),
        )

        buffer_catalog.add(essence_book)

    return list(buffer_catalog.data.values())
