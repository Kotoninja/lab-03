import json
from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path

import pytest
from pytest import MonkeyPatch

from src.catalog import Catalog
from src.errors import DamagedFile, UnsupportedFormatVersion
from src.models import BookModel

BOOK = BookModel(
    id="book-1",
    title="Мастер и Маргарита",
    category="Fiction",
    timestamp=datetime(2026, 1, 2, 10, tzinfo=UTC),
    author="Михаил Булгаков",
    price=Decimal("15.75"),
)


def create_json(tmp_path: Path, document) -> Path:
    path = tmp_path / "catalog.json"
    path.write_text(
        json.dumps(document, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return path


def test_catalog(tmp_path, monkeypatch: MonkeyPatch):
    monkeypatch.setattr("src.repository.RESULTS_DIR", tmp_path)

    catalog = Catalog()
    catalog.add(BOOK)

    saved_file = tmp_path / "save_1.json"
    catalog.save(Path(saved_file.name))

    restored = Catalog()
    restored.load(saved_file)

    assert list(restored) == [BOOK]

    saved = json.loads(saved_file.read_text(encoding="utf-8"))

    assert saved["format_version"] == 1
    assert saved["data"][BOOK.id]["price"] == "15.75"
    assert saved["data"][BOOK.id]["title"] == "Мастер и Маргарита"
    assert saved["data"][BOOK.id]["category"] == "Fiction"
    assert saved["data"][BOOK.id]["author"] == "Михаил Булгаков"
    assert saved["data"][BOOK.id]["timestamp"] == "2026-01-02T10:00:00+00:00"


def test_empty_catalog_json(tmp_path, monkeypatch: MonkeyPatch):
    monkeypatch.setattr("src.repository.RESULTS_DIR", tmp_path)
    document = {"format_version": 1, "data": {}}
    file = create_json(tmp_path, document)

    catalog = Catalog()
    catalog.load(file)

    saved_file = tmp_path / "save_1.json"
    catalog.save(Path(saved_file.name))

    assert json.loads(saved_file.read_text(encoding="utf-8")) == document

    restored = Catalog()
    restored.load(saved_file)

    assert list(restored) == []


def test_invalid_version(tmp_path, monkeypatch: MonkeyPatch):
    monkeypatch.setattr("src.repository.RESULTS_DIR", tmp_path)

    document = {"format_version": 2, "data": {}}
    file = create_json(tmp_path, document)

    catalog = Catalog()

    with pytest.RaisesExc(UnsupportedFormatVersion):
        catalog.load(file)


def test_with_damage_file(tmp_path):
    file: Path = tmp_path / "damage.json"
    file.write_text('"format_version":1, "data": {"test"')

    catalog = Catalog()
    catalog.add(BOOK)

    with pytest.RaisesExc(DamagedFile):
        catalog.load(file)

    assert len(catalog) == 1


def test_with_no_format_version(tmp_path):
    file: Path = tmp_path / "damage.json"
    file.write_text('"data": {"test"}')

    catalog = Catalog()
    catalog.add(BOOK)

    with pytest.RaisesExc(DamagedFile):
        catalog.load(file)


@pytest.mark.parametrize("field", ["id", "title", "category", "timestamp", "author", "price"])
def test_load_book_missing_required_field(tmp_path, field):
    book_data = {
        "id": "1",
        "title": "Pride and Prejudice",
        "category": "Fiction",
        "timestamp": "2026-01-01T10:00:00+00:00",
        "author": "Jane Austen",
        "price": "12.50",
    }
    del book_data[field]
    file = create_json(tmp_path, {"format_version": 1, "data": {"1": book_data}})

    with pytest.raises(DamagedFile):
        Catalog().load(file)


def test_data_not_dict(tmp_path):
    file: Path = tmp_path / "damage.json"
    file.write_text('"format_version":1,"data": 23')
    catalog = Catalog()
    with pytest.RaisesExc(DamagedFile):
        catalog.load(file)

def test_format_version_not_int(tmp_path):
    file: Path = tmp_path / "damage.json"
    file.write_text('"format_version":{},"data": 23')
    catalog = Catalog()
    with pytest.RaisesExc(DamagedFile):
        catalog.load(file)

def test_book_instance_with_not_tz_timestamp(tmp_path):
    book_data = {
        "id": "1",
        "title": "Pride and Prejudice",
        "category": "Fiction",
        "timestamp": "2026-01-01",
        "author": "Jane Austen",
        "price": "12.50",
    }

    file = create_json(tmp_path, {"format_version": 1, "data": {"1": book_data}})
    catalog = Catalog()
    with pytest.RaisesExc(DamagedFile):
        catalog.load(file)
