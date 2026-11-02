"""Каталог книг: модель Book и заглушка BookCatalog (задача T-1)."""

from dataclasses import dataclass


@dataclass
class Book:
    """Книга в каталоге библиотеки."""

    isbn: str
    title: str
    author: str
    year: int
    total_copies: int = 1
    available_copies: int = 1


class BookCatalog:
    """Каталог книг. Данные хранятся в памяти (минимальная реализация)."""

    def __init__(self) -> None:
        self._books: dict[str, Book] = {}

    def add_book(self, book: Book) -> None:
        """Добавить книгу. ISBN должен быть уникальным (BR-7)."""
        if book.isbn in self._books:
            raise ValueError(f"Книга с ISBN {book.isbn} уже есть в каталоге")
        self._books[book.isbn] = book

    def find_by_isbn(self, isbn: str) -> Book | None:
        """Найти книгу по ISBN, вернуть None, если книги нет."""
        return self._books.get(isbn)

    def find_by_title(self, query: str) -> list[Book]:
        """Найти книги, в названии которых есть строка поиска (без учёта регистра)."""
        query = query.lower()
        return [b for b in self._books.values() if query in b.title.lower()]

    def remove_book(self, isbn: str) -> None:
        """Удалить книгу из каталога. Заглушка: будет реализована в задаче B-4."""
        raise NotImplementedError("Удаление книги будет реализовано позже")
