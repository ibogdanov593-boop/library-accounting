import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from library.book_catalog import Book, BookCatalog  # noqa: E402


class BookCatalogTest(unittest.TestCase):
    def setUp(self) -> None:
        self.catalog = BookCatalog()
        self.book = Book("978-5-17-000001-1", "Война и мир", "Л. Толстой", 1869)

    def test_add_and_find_by_isbn(self) -> None:
        self.catalog.add_book(self.book)
        self.assertEqual(self.catalog.find_by_isbn(self.book.isbn), self.book)

    def test_find_unknown_isbn_returns_none(self) -> None:
        self.assertIsNone(self.catalog.find_by_isbn("000"))

    def test_duplicate_isbn_rejected(self) -> None:
        self.catalog.add_book(self.book)
        with self.assertRaises(ValueError):
            self.catalog.add_book(self.book)

    def test_find_by_title_ignores_case(self) -> None:
        self.catalog.add_book(self.book)
        self.assertEqual(self.catalog.find_by_title("МИР"), [self.book])

    def test_remove_book_is_stub(self) -> None:
        with self.assertRaises(NotImplementedError):
            self.catalog.remove_book(self.book.isbn)


if __name__ == "__main__":
    unittest.main()
