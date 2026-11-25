import json
from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path

import pytest
from pytest import MonkeyPatch

from src.catalog import Catalog
from src.errors import DamagedFile
from src.models import BookModel
from src.repository import Storage


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

    storage = Storage()
    storage.save(catalog)
    saved_file = tmp_path / "save_1.json"

    assert storage.load(saved_file) == [BOOK]
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
    storage = Storage()
    catalog = Catalog()
    catalog.update(storage.load(file))

    storage.save(catalog)
    saved_file = tmp_path / "save_1.json"

    assert json.loads(saved_file.read_text(encoding="utf-8")) == document
    assert storage.load(saved_file) == []


def test_invalid_version(tmp_path, monkeypatch: MonkeyPatch):
    monkeypatch.setattr("src.repository.RESULTS_DIR", tmp_path)

    document = {"version": 2, "data": {}}
    file = create_json(tmp_path, document)

    storage = Storage()
    catalog = Catalog()

    with pytest.RaisesExc(DamagedFile):
        catalog.update(storage.load(file))


def test_with_damage_file(tmp_path):
    file: Path = tmp_path / "damage.json"

    file.write_text('"format_version":1, "data": {"test"')

    storage = Storage()
    catalog = Catalog()

    catalog.add(BOOK)

    with pytest.RaisesExc(DamagedFile):
        catalog.update(storage.load(file))

    assert len(catalog) == 1
