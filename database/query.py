import sqlite3
from typing import Optional

from .common import (
    AUTHORS_TABLE_NAME,
    BOOK_AUTHORS_TABLE_NAME,
    BOOK_LOANS_TABLE_NAME,
    BOOKS_TABLE_NAME,
    BORROWERS_TABLE_NAME,

    Author,
    Book,
    Borrower,
    Fine,
    Loan,
)

from . import config

def get_one_or_none(sql: str, params: list) -> Optional[tuple]:
    conn = sqlite3.connect(config.db_name)
    c = conn.cursor()

    c.execute(sql, params)
    result = c.fetchone()

    conn.close()

    if not result:
        return None

    return result

def get_all_or_none(sql: str, params: list) -> Optional[list[tuple]]:
    conn = sqlite3.connect(config.db_name)
    c = conn.cursor()

    c.execute(sql, params)
    result = c.fetchall()

    conn.close()

    if not result:
        return None

    return result

def search(query: str) -> list:
    if not query:
        return []

    conn = sqlite3.connect(config.db_name)
    c = conn.cursor()

    sql = f"""
    SELECT
        b.Isbn as Isbn,
        b.Title as Title,
        GROUP_CONCAT(a.Name, ', ') as Authors,
        CASE
            WHEN l.Isbn IS NULL THEN 1
            WHEN l.Date_in IS NOT NULL THEN 1
            ELSE 0
        END as Status
    FROM {BOOKS_TABLE_NAME} b
    LEFT JOIN {BOOK_AUTHORS_TABLE_NAME} ba ON ba.Isbn = b.Isbn
    LEFT JOIN {AUTHORS_TABLE_NAME} a ON a.Author_id = ba.Author_id
    LEFT JOIN {BOOK_LOANS_TABLE_NAME} l ON b.Isbn = l.Isbn AND l.Date_in IS NULL
    WHERE b.Isbn LIKE ? COLLATE NOCASE
       OR b.Title LIKE ? COLLATE NOCASE
       OR a.Name LIKE ? COLLATE NOCASE
    GROUP BY b.Isbn, b.Title, l.Isbn, l.Date_in
    """
    params = [f"%{query}%" for _ in range(3)]

    c.execute(sql, params)
    results = c.fetchall()

    conn.close()

    return results

def book_exists(isbn: str) -> bool:
    return find_book(isbn) is not None

def book_available(isbn: str) -> bool:
    sql = f"""
    SELECT
        COUNT(*) as n_checkouts
    FROM {BOOK_LOANS_TABLE_NAME}
    WHERE Isbn = ?
      AND Date_in IS NULL
    """

    return bool(get_one_or_none(sql, [isbn]))

def find_book(isbn: str) -> Optional[Book]:
    sql = f"""
    SELECT
        Isbn,
        Title
    FROM {BOOKS_TABLE_NAME}
    WHERE Isbn = ?
    """

    return get_one_or_none(sql, [isbn])

def find_author(author_id: str) -> Optional[Author]:
    sql = f"""
    SELECT
        Author_id,
        Name
    FROM {AUTHORS_TABLE_NAME}
    WHERE Author_id = ?
    """

    return get_one_or_none(sql, [author_id])

def find_borrower_by_ssn(ssn: str) -> Optional[Borrower]:
    sql = f"""
    SELECT
        Card_id,
        Ssn,
        Bname,
        Address,
        Phone
    FROM {BORROWERS_TABLE_NAME}
    WHERE Ssn = ?
    """

    return get_one_or_none(sql, [ssn])

def find_borrower_by_id(borrower_id: str) -> Optional[Borrower]:
    sql = f"""
    SELECT
        Card_id,
        Ssn,
        Bname,
        Address,
        Phone
    FROM {BORROWERS_TABLE_NAME}
    WHERE Card_id = ?
    """

    return get_one_or_none(sql, [borrower_id])

def get_loans(borrower_id: str) -> Optional[list[Loan]]:
    sql = f"""
    """

    params = []

    return get_all_or_none(sql, params)

def get_fines(borrower_id: str) -> Optional[list[Fine]]:
    sql = f"""
    """

    params = []

    return get_all_or_none(sql, params)
