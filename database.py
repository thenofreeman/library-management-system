import sqlite3

from common import (
    DB_NAME,
    BOOK_TABLE,
    BOOK_AUTHORS_TABLE,
    AUTHORS_TABLE,
    BORROWER_TABLE,
    BOOK_LOANS_TABLE,
    FINES_TABLE
)
from logger import logger

def write_books(data: list[list[str]]) -> None:
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    sql = f"""INSERT INTO {BOOK_TABLE} (
        Isbn, Title
    ) VALUES (
        ?, ?
    );"""

    book_data = [tuple(row) for row in data[1:]]

    try:
        c.executemany(sql, book_data)
        conn.commit()
    except sqlite3.Error as e:
        logger.error(e.__str__())

        conn.rollback()

    conn.close()

def write_book_authors(data: list[list[str]]) -> None:
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # TODO: shouldn't ignore... there is an issue with the normalize code
    sql = f"""INSERT OR IGNORE INTO {BOOK_AUTHORS_TABLE} (
        Author_id, Isbn
    ) VALUES (
        ?, ?
    );"""

    book_authors_data = [tuple(row) for row in data[1:]]

    try:
        c.executemany(sql, book_authors_data)
        conn.commit()
    except sqlite3.Error as e:
        logger.error(e.__str__())

        conn.rollback()

    conn.close()

def write_authors(data: list[list[str]]) -> None:
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    sql = f"""INSERT INTO {AUTHORS_TABLE} (
        Author_id, Name
    ) VALUES (
        ?, ?
    );"""

    authors_data = [tuple(row) for row in data[1:]]

    try:
        c.executemany(sql, authors_data)
        conn.commit()
    except sqlite3.Error as e:
        logger.error(e.__str__())

        conn.rollback()

    conn.close()

def write_borrowers(data: list[list[str]]) -> None:
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    sql = f"""INSERT INTO {BORROWER_TABLE} (
        Card_id, Ssn, Bname, Address, Phone
    ) VALUES (
        ?, ?, ?, ?, ?
    );"""

    borrowers_data = [tuple(row) for row in data[1:]]

    try:
        c.executemany(sql, borrowers_data)
        conn.commit()
    except sqlite3.Error as e:
        logger.error(e.__str__())

        conn.rollback()

    conn.close()
