from dataclasses import replace
from datetime import UTC, datetime
from decimal import Decimal
from unittest import TestCase

from src.catalog import Catalog
from src.errors import DuplicateID, InvalidEssence, ObjectNotFound
from src.models import BookModel


class TestCatalog(TestCase):
    def setUp(self):
        self.catalog = Catalog()
        self.book = BookModel(
            id="book-1",
            title="Pride and Prejudice",
            category="Fiction",
            timestamp=datetime(2026, 1, 1, tzinfo=UTC),
            author="Jane Austen",
            price=Decimal("12.50"),
        )

    def test_add(self):
        self.catalog.add(self.book)
        self.assertIn(self.book.id, self.catalog)
        self.assertEqual(len(self.catalog), 1)
        with self.assertRaises(DuplicateID):
            self.catalog.add(self.book)

    def test_get(self):
        self.catalog.add(self.book)
        self.assertEqual(self.catalog.get(self.book.id), self.book)
        with self.assertRaises(ObjectNotFound):
            self.catalog.get("missing")

    def test_remove(self):
        self.catalog.add(self.book)
        self.catalog.remove(self.book.id)
        self.assertNotIn(self.book.id, self.catalog)
        with self.assertRaises(ObjectNotFound):
            self.catalog.remove(self.book.id)

    def test_update(self):
        second_book = replace(self.book, id="book-2", title="Sense and Sensibility")
        self.catalog.update([self.book, second_book])
        self.assertEqual(self.catalog.get(self.book.id), self.book)
        self.assertEqual(self.catalog.get(second_book.id), second_book)

    def test_iteration_follows_insertion_order(self):
        second_book = replace(self.book, id="book-2", title="Sense and Sensibility")
        self.catalog.add(second_book)
        self.catalog.add(self.book)
        self.assertEqual(list(self.catalog), [second_book, self.book])

    def test_find_by_category(self):
        self.catalog.add(self.book)
        self.assertEqual(self.catalog.find_by_category("Fiction"), [self.book])
        with self.assertRaises(ObjectNotFound):
            self.catalog.find_by_category("Science")

    def test_find_by_name(self):
        self.catalog.add(self.book)
        self.assertEqual(self.catalog.find_by_name("pride and prejudice"), self.book)
        self.assertEqual(self.catalog.find_by_name("PRIDE and Prejudice"), self.book)
        with self.assertRaises(ObjectNotFound):
            self.catalog.find_by_name("Missing title")

    def test_with_object(self):
        with self.assertRaises(InvalidEssence):
            self.catalog.add(object())

    