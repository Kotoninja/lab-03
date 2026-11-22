from dataclasses import replace
from datetime import UTC, datetime
from decimal import Decimal
from unittest import TestCase

from src.errors import InvalidEssence
from src.models import BookModel


class TestBookModel(TestCase):
    def setUp(self):
        self.book = BookModel(
            id="book-1",
            title="Pride and Prejudice",
            category="Fiction",
            timestamp="2026-10-12T00:00:00+00:00",
            author="Jane Austen",
            price=Decimal("12.50"),
        )

    def test_id(self):
        self.assertEqual(self.book.id, "book-1")
        with self.assertRaises(InvalidEssence):
            replace(self.book, id="")

    def test_title(self):
        self.assertEqual(self.book.title, "Pride and Prejudice")
        with self.assertRaises(InvalidEssence):
            replace(self.book, title="")
        with self.assertRaises(InvalidEssence):
            replace(self.book, title="\t")

    def test_category(self):
        self.assertEqual(self.book.category, "Fiction")
        with self.assertRaises(InvalidEssence):
            replace(self.book, category="")
        with self.assertRaises(InvalidEssence):
            replace(self.book, category="\t")

    def test_timestamp(self):
        self.assertEqual(self.book.timestamp, datetime(2026, 10, 12, tzinfo=UTC))

        timestamp = datetime(2026, 1, 1, tzinfo=UTC)
        book = replace(self.book, timestamp=timestamp)

        self.assertEqual(book.timestamp, timestamp)

    def test_author(self):
        self.assertEqual(self.book.author, "Jane Austen")
        with self.assertRaises(InvalidEssence):
            replace(self.book, author="")
        with self.assertRaises(InvalidEssence):
            replace(self.book, author="\t")

    def test_price(self):
        self.assertEqual(self.book.price, Decimal("12.50"))
        with self.assertRaises(InvalidEssence):
            replace(self.book, price=Decimal("0.0"))
