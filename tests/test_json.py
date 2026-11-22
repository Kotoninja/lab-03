import json
from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path

from pytest import MonkeyPatch

from src.catalog import Catalog
from src.models import BookModel
from src.repository import Storage


def create_json_file(tmp_path: Path, document) -> Path:
    path = tmp_path / "catalog.json"
    path.write_text(
        json.dumps(document, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return path


def test_catalog_json_round_trip(tmp_path: Path, monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr("src.repository.RESULTS_DIR", tmp_path)
    book = BookModel(
        id="book-1",
        title="Мастер и Маргарита",
        category="Fiction",
        timestamp=datetime(2026, 1, 2, 10, tzinfo=UTC),
        author="Михаил Булгаков",
        price=Decimal("15.75"),
    )
    catalog = Catalog()
    catalog.add(book)

    storage = Storage()
    storage.save(catalog)
    saved_file = tmp_path / "save_1.json"

    assert storage.load(saved_file) == [book]
    saved = json.loads(saved_file.read_text(encoding="utf-8"))
    assert saved["format_version"] == 1
    assert saved["data"][book.id]["price"] == "15.75"
    assert saved["data"][book.id]["title"] == "Мастер и Маргарита"
    assert saved["data"][book.id]["category"] == "Fiction"
    assert saved["data"][book.id]["author"] == "Михаил Булгаков"
    assert saved["data"][book.id]["timestamp"] == "2026-01-02T10:00:00+00:00"


def test_empty_catalog_json_round_trip(
    tmp_path: Path, monkeypatch: MonkeyPatch
) -> None:
    monkeypatch.setattr("src.repository.RESULTS_DIR", tmp_path)
    document = {"format_version": 1, "data": {}}
    source = create_json_file(tmp_path, document)
    storage = Storage()
    catalog = Catalog()
    catalog.update(storage.load(source))

    storage.save(catalog)
    saved_file = tmp_path / "save_1.json"

    assert json.loads(saved_file.read_text(encoding="utf-8")) == document
    assert storage.load(saved_file) == []
