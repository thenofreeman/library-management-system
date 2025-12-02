import sqlite3
from pathlib import Path
from typing import Optional
import os

from .common import (
    BOOKS_TABLE_NAME,
    BOOK_AUTHORS_TABLE_NAME,
    AUTHORS_TABLE_NAME,
    BORROWERS_TABLE_NAME,
    BOOK_LOANS_TABLE_NAME,
    FINES_TABLE_NAME,
    METADATA_TABLE_NAME,

    StringMatrix,
    CSVData,
)

from . import config

from logger import Logger

def init(db_name: str) -> bool:
    config.set_db_name(db_name)

    data = _import_data_from_csv()

    if not data:
        return False

    created = _create_database()

    if not created:
        return False

    return _insert_data(data)

def exists(db_name: str) -> bool:
    return Path(db_name).is_file()

def delete(db_name: str) -> bool:
    if os.path.exists(db_name):
        os.remove(db_name)

        return True

    return False

def _create_database() -> bool:
    print(config.db_name)

    conn = sqlite3.connect(config.db_name)
    c = conn.cursor()

    c.execute(f"""
        CREATE TABLE {BOOKS_TABLE_NAME} (
            Isbn TEXT NOT NULL,
            Title TEXT NOT NULL,

            PRIMARY KEY (Isbn)
        );
    """)

    c.execute(f"""
        CREATE TABLE {BOOK_AUTHORS_TABLE_NAME} (
            Author_id TEXT NOT NULL,
            Isbn TEXT NOT NULL,

            PRIMARY KEY(Author_id, Isbn),

            FOREIGN KEY(Author_id) REFERENCES AUTHORS(Author_id),
            FOREIGN KEY(Isbn) REFERENCES BOOK(Isbn)
        );
    """)

    c.execute(f"""
        CREATE TABLE {AUTHORS_TABLE_NAME} (
            Author_id TEXT NOT NULL,
            Name TEXT NOT NULL,

            PRIMARY KEY (Author_id)
        );
    """)

    c.execute(f"""
        CREATE TABLE {BORROWERS_TABLE_NAME} (
            Card_id INTEGER PRIMARY KEY AUTOINCREMENT,
            Ssn TEXT NOT NULL,
            Bname TEXT NOT NULL,
            Address TEXT NOT NULL,
            Phone TEXT
        );
    """)

    c.execute(f"""
        CREATE TABLE {BOOK_LOANS_TABLE_NAME} (
            Loan_id INTEGER PRIMARY KEY AUTOINCREMENT,
            Isbn TEXT NOT NULL,
            Card_id INTEGER NOT NULL,
            Date_out TEXT NOT NULL,
            Date_in TEXT,

            FOREIGN KEY(Isbn) REFERENCES BOOK(Isbn),
            FOREIGN KEY(Card_id) REFERENCES BORROWER(Card_id)
        );
    """)

    c.execute(f"""
        CREATE TABLE {FINES_TABLE_NAME} (
            Loan_id INTEGER NOT NULL,
            Fine_amt INTEGER NOT NULL,
            Paid INTEGER NOT NULL,

            PRIMARY KEY (Loan_id),

            FOREIGN KEY(Loan_id) REFERENCES BOOK_LOANS(Loan_id)
        );
    """)

    c.execute(f"""
        CREATE TABLE IF NOT EXISTS {METADATA_TABLE_NAME} (
            key TEXT PRIMARY KEY,
            value TEXT
        );
    """)

    conn.close()

    return True

def _insert_data(data: CSVData) -> bool:
    (books, book_authors, authors, borrowers) = data

    conn = sqlite3.connect(config.db_name)
    c = conn.cursor()

    def try_insert(sql_query: str, data_values) -> bool:
        # TODO: logging

        try:
            c.executemany(sql_query, data_values)
            conn.commit()
        except sqlite3.Error as e:
            conn.rollback()

            return False

        return True

    def insert_books() -> bool:
        sql = f"""INSERT INTO {BOOKS_TABLE_NAME} (
            Isbn, Title
        ) VALUES (
            ?, ?
        );"""

        book_data = [tuple(row) for row in books[1:]]

        return try_insert(sql, book_data)

    def insert_book_authors() -> bool:
        # TODO: shouldn't ignore... there is an issue with the normalize code
        sql = f"""INSERT OR IGNORE INTO {BOOK_AUTHORS_TABLE_NAME} (
            Author_id, Isbn
        ) VALUES (
            ?, ?
        );"""

        book_authors_data = [tuple(row) for row in book_authors[1:]]

        return try_insert(sql, book_authors_data)

    def insert_authors() -> bool:
        sql = f"""INSERT INTO {AUTHORS_TABLE_NAME} (
            Author_id, Name
        ) VALUES (
            ?, ?
        );"""

        authors_data = [tuple(row) for row in authors[1:]]

        return try_insert(sql, authors_data)

    def insert_borrowers() -> bool:
        sql = f"""INSERT INTO {BORROWERS_TABLE_NAME} (
            Ssn, Bname, Address, Phone
        ) VALUES (
            ?, ?, ?, ?
        );"""

        borrowers_data = [tuple(row[1:]) for row in borrowers]

        return try_insert(sql, borrowers_data)

    insert_successes = [insert_books(),
                        insert_book_authors(),
                        insert_authors(),
                        insert_borrowers()]

    conn.close()

    return all(insert_successes)

def _import_data_from_csv() -> Optional[CSVData]:
    import csv

    def read_borrowers() -> Optional[StringMatrix]:
        # borrowers_data = [['Card_id', 'Ssn', 'Bname', 'Address', 'Phone']]
        borrowers_result: StringMatrix = []

        try:
            with open('data/borrower.csv', 'r', encoding='utf-8') as file:
                rows = list(csv.reader(file))
                header = rows[0]

                for row in rows[1:]:
                    [idn, ssn, fname, lname, email, addr, city, state, phone] = row
                    full_name = f'{fname} {lname}'
                    address = f'{addr}, {city}, {state}'

                    new_borrower = [int(idn[2:]), ssn, full_name, address, phone]
                    borrowers_result.append(new_borrower)

        except FileNotFoundError:
            return None

        return sorted(borrowers_result, key=lambda x: x[0])

    def read_books() -> Optional[tuple[StringMatrix, StringMatrix, StringMatrix]]:
        # books_data = [['Isbn', 'Title']]
        # authors_data = [['Author_id', 'Name']]
        # book_authors_data = [['Author_id', 'Isbn']]
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

    books_data = read_books()
    borrowers_data = read_borrowers()

    if not (books_data and borrowers_data):
        return None

    (books, book_authors, authors) = books_data
    borrowers = borrowers_data

    return (books, book_authors, authors, borrowers)
