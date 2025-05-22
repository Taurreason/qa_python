import pytest
from main import BooksCollector


class TestBooksCollector:

    def test_add_new_book_only_once(self):
        collector = BooksCollector()
        collector.add_new_book('Цветы для элджернона')
        collector.add_new_book('Цветы для элджернона')

        assert 'Цветы для элджернона' in collector.books_genre
        assert list(collector.books_genre.keys()).count('Цветы для элджернона') == 1

    def test_add_new_book_len_max40(self):
        collector = BooksCollector()
        valid_name_book = 'A' * 40
        collector.add_new_book(valid_name_book)
        assert valid_name_book in collector.books_genre

    def test_add_new_book_len_more_than40(self):
        collector = BooksCollector()
        invalid_name_book = 'В' * 41
        collector.add_new_book(invalid_name_book)
        assert invalid_name_book not in collector.books_genre

    def test_add_new_book_empty_name(self):
        collector = BooksCollector()
        collector.add_new_book('')
        assert collector.books_genre == {}

    def test_set_book_genre_non_existent_book(self):
        collector = BooksCollector()
        collector.set_book_genre('Несуществующая', 'Ужасы')
        assert 'Несуществующая' not in collector.books_genre

    def test_set_book_genre(self):
        collector = BooksCollector()
        collector.add_new_book('Дюна')
        collector.set_book_genre('Дюна', 'Фантастика')
        assert collector.books_genre.get('Дюна') == 'Фантастика'

    def test_set_book_genre_non_existent_genre(self):
        collector = BooksCollector()
        collector.add_new_book('Маленькая жизнь')
        collector.set_book_genre('Маленькая жизнь', 'Драма')
        assert collector.books_genre.get('Маленькая жизнь') == ''

    def test_set_book_genre_empty_string(self):
        collector = BooksCollector()
        collector.add_new_book('Собачье сердце')
        collector.set_book_genre('Собачье сердце', '')
        assert collector.books_genre.get('Собачье сердце') == ''

    def test_get_book_genre_all_genre(self, collector_with_book_and_genre):
        collector, book, genre = collector_with_book_and_genre
        assert collector.get_book_genre(book) == genre

    def test_get_book_genre_non_existing(self):
        collector = BooksCollector()
        assert collector.get_book_genre('Несуществующая') is None

    def test_get_books_with_specific_genre_single(self, collector_with_book_and_genre):
        collector, book, genre = collector_with_book_and_genre
        assert collector.get_books_with_specific_genre(genre) == [book]

    def test_get_books_with_specific_genre_multiple(self):
        collector = BooksCollector()
        for title in ['Сияние', 'Оно', 'Мизери']:
            collector.add_new_book(title)
            collector.set_book_genre(title, 'Ужасы')
        result = collector.get_books_with_specific_genre('Ужасы')
        assert set(result) == {'Сияние', 'Оно', 'Мизери'}

    def test_get_books_genre_returns_dict(self):
        collector = BooksCollector()
        collector.add_new_book('Сияние')
        assert collector.get_books_genre() == {'Сияние': ''}

    @pytest.mark.parametrize('book, genre', [
        ('Гарри Поттер', 'Фантастика'),
        ('Винни-Пух', 'Мультфильмы'),
        ('Большой Лебовски', 'Комедии')])
    def test_get_books_for_children_allowed_genres(self, book, genre):
        collector = BooksCollector()
        collector.add_new_book(book)
        collector.set_book_genre(book, genre)
        assert collector.get_books_for_children() == [book]

    @pytest.mark.parametrize('book, genre', [('Сияние', 'Ужасы'), ('Шерлок Холмс', 'Детективы')])
    def test_get_books_for_children_age_restricted(self, book, genre):
        collector = BooksCollector()
        collector.add_new_book(book)
        collector.set_book_genre(book, genre)
        assert collector.get_books_for_children() == []

    def test_add_book_in_favorites_book_in_books_genre(self, collector_with_book_and_genre):
        collector, book, genre = collector_with_book_and_genre
        collector.add_book_in_favorites(book)

        assert book in collector.favorites

    def test_add_book_in_favorites_only_once(self):
        collector = BooksCollector()
        collector.add_new_book('1+1')
        collector.set_book_genre('1+1', 'Комедия')
        collector.add_book_in_favorites('1+1')
        collector.add_book_in_favorites('1+1')

        assert collector.favorites.count('1+1') == 1

    def test_add_book_in_favorites_the_same_book(self):
        collector = BooksCollector()
        collector.add_book_in_favorites('Неизвестная книга')

        assert collector.favorites == []

    def test_delete_book_from_favorites_existing(self, collector_with_book_and_genre):
        collector, book, genre = collector_with_book_and_genre
        collector.add_book_in_favorites(book)
        collector.delete_book_from_favorites(book)

        assert book not in collector.favorites

    def test_get_list_of_favorites_books(self, collector_with_book_and_genre):
        collector, book, genre = collector_with_book_and_genre
        collector.add_book_in_favorites(book)

        assert collector.get_list_of_favorites_books() == [book]
