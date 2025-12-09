import html
import csv
from typing import Optional

from database.dtypes import CSVData, StringMatrix

def from_csv() -> Optional[CSVData]:

    books_data = _read_books()
    borrowers_data = _read_borrowers()

    if not (books_data and borrowers_data):
        return None

    (books, book_authors, authors) = books_data
    borrowers = borrowers_data

    return (books, book_authors, authors, borrowers)

def _read_borrowers() -> Optional[StringMatrix]:
    # borrowers_data = [['Card_id', 'Ssn', 'Bname', 'Address', 'Phone']]
    borrowers_result: StringMatrix = []

    try:
        with open('data/borrower.csv', 'r', encoding='utf-8') as file:
            rows = list(csv.reader(file))
            header = rows[0]

            for row in rows[1:]:
                row = [html.unescape(field) for field in row]

                [idn, ssn, fname, lname, email, addr, city, state, phone] = row
                full_name = f'{fname} {lname}'
                address = f'{addr}, {city}, {state}'

                new_borrower = [int(idn[2:]), ssn, full_name, address, phone]
                borrowers_result.append(new_borrower)

    except FileNotFoundError:
        return None

    return sorted(borrowers_result, key=lambda x: x[0])

def _read_books() -> Optional[tuple[StringMatrix, StringMatrix, StringMatrix]]:
    books_data: StringMatrix = []
    authors_data: StringMatrix = []
    book_authors_data: StringMatrix = []

    try:
        with open('data/book.csv', 'r', encoding='utf-8') as file:
            rows = list(csv.reader(file, delimiter='\t'))
            header = rows[0]

            author_id_incr = 0
            author_set = dict()

            for row in rows[1:]:
                row = [html.unescape(field) for field in row]

                [isbn10, isbn13, title, authors, cover, pub, pages] = row

                new_book = [isbn10, title]
                books_data.append(new_book)

                for author in authors.split(','):
                    author = author.strip()

                    if author == '':
                        author = 'Unknown Author'

                    if author not in author_set:
                        author_set[author] = author_id_incr
                        author_id_incr += 1

                    new_book_author = [author_set[author], isbn10]
                    book_authors_data.append(new_book_author)

            for (name, author_id) in author_set.items():
                new_author = [author_id, name]
                authors_data.append(new_author)

    except FileNotFoundError:
        return None

    return (books_data, book_authors_data, authors_data)

def load_additional_test_data(db_name: str) -> bool:
    # TODO: ...
    return False
