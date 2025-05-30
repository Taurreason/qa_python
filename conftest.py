import pytest

from tests import BooksCollector


@pytest.fixture(params=[
    ('Гарри Поттер', 'Фантастика'),
    ('Сияние', 'Ужасы'),
    ('Шерлок Холмс', 'Детективы'),
    ('Винни-Пух', 'Мультфильмы'),
    ('Большой Лебовски', 'Комедии')
])
def book_and_genre(request):
    return request.param


@pytest.fixture
def collector_with_book_and_genre(book_and_genre):
    book, genre = book_and_genre
    collector = BooksCollector()
    collector.add_new_book(book)
    collector.set_book_genre(book, genre)
    return collector, book, genre