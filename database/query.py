import sqlite3
from typing import Optional
from datetime import date

from .common import (
    AUTHORS_TABLE_NAME,
    BOOK_AUTHORS_TABLE_NAME,
    BOOK_LOANS_TABLE_NAME,
    BOOKS_TABLE_NAME,
    BORROWERS_TABLE_NAME,
    FINES_TABLE_NAME,

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

def search_books(query: str) -> Optional[list[Book]]:
    if not query:
        return []

    sql = f"""
    SELECT
        b.Isbn as Isbn,
        b.Title as Title,
        GROUP_CONCAT(a.Name, ', ') as Authors,
        CASE
            WHEN l.Isbn IS NULL THEN 1
            WHEN l.Date_in IS NULL THEN 0
            ELSE 1
        END as Status
    FROM {BOOKS_TABLE_NAME} b
    LEFT JOIN {BOOK_AUTHORS_TABLE_NAME} ba ON ba.Isbn = b.Isbn
    LEFT JOIN {AUTHORS_TABLE_NAME} a ON a.Author_id = ba.Author_id
    LEFT JOIN {BOOK_LOANS_TABLE_NAME} l ON b.Isbn = l.Isbn
    WHERE b.Isbn LIKE ? COLLATE NOCASE
       OR b.Title LIKE ? COLLATE NOCASE
       OR a.Name LIKE ? COLLATE NOCASE
    GROUP BY b.Isbn, b.Title, l.Isbn, l.Date_in
    """
    params = [f"%{query}%" for _ in range(3)]

    return get_all_or_none(sql, params)

def search_checkouts(isbn: str | None = None,
                     borrower_id: str | None = None,
                     name: str | None = None,
                     returned: bool | None = None) -> Optional[list[Loan]]:
    sql = f"""
    SELECT
        l.Loan_id,
        l.Isbn,
        b.Title,
        l.Card_id,
        br.Bname,
        l.Date_out,
        l.Date_in
    FROM BOOK_LOANS l
    JOIN BOOK b ON b.Isbn = l.Isbn
    JOIN BORROWER br ON br.Card_id = l.Card_id
    WHERE l.Date_in IS NULL
      {'' if returned else 'AND l.Date_in IS NULL'}
    """

    conditions = []
    params = []

    if isbn:
        conditions.append("l.Isbn LIKE ? COLLATE NOCASE")
        params.append(f"%{isbn}%")

    if borrower_id:
        conditions.append("br.Card_id LIKE ?")
        params.append(f"%{isbn}%")

    if name:
        conditions.append("br.Bname LIKE ? COLLATE NOCASE")
        params.append(f"%{isbn}%")

    if conditions:
        sql += " AND (" + " OR ".join(conditions) + ")"

    sql += " ORDER BY l.Date_out DESC"

    return get_all_or_none(sql, params)

def book_exists(isbn: str) -> bool:
    return get_book(isbn) is not None

def book_available(isbn: str) -> bool:
    sql = f"""
    SELECT
        COUNT(*) as n_checkouts
    FROM {BOOK_LOANS_TABLE_NAME}
    WHERE Isbn = ?
      AND Date_in IS NULL
    """

    return bool(get_one_or_none(sql, [isbn]))

def get_book(isbn: str) -> Optional[Book]:
    books = search_books(isbn)

    if not books:
        return None

    return books[0]

def get_author(author_id: str) -> Optional[Author]:
    sql = f"""
    SELECT
        Author_id,
        Name
    FROM {AUTHORS_TABLE_NAME}
    WHERE Author_id = ?
    """

    return get_one_or_none(sql, [author_id])

def get_borrower_by_ssn(ssn: str) -> Optional[Borrower]:
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

def get_borrower_by_id(borrower_id: str) -> Optional[Borrower]:
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

def get_loans(borrower_id: str, returned: bool = False) -> Optional[list[Loan]]:
    return search_checkouts(borrower_id=borrower_id, returned=returned)

def get_fines(borrower_id: str | None = None, unpaid: bool = False) -> Optional[list[Fine]]:
    where_clause = "WHERE " if (borrower_id or unpaid) else ''

    if borrower_id:
        where_clause += 'l.Card_id = ?'

    if unpaid:
        if borrower_id:
            where_clause += ' AND '

        where_clause += 'f.Paid = 0'

    sql = f"""
    SELECT
        f.Loan_id,
        f.Fine_amt,
        b.Isbn,
        f.Paid
    FROM {FINES_TABLE_NAME} f
    JOIN {BOOK_LOANS_TABLE_NAME} l ON l.Loan_id = f.Loan_id
    JOIN {BOOKS_TABLE_NAME} b ON b.Isbn = l.Isbn
    {where_clause}
    ORDER BY l.Date_out DESC
    """

    params = [borrower_id] if borrower_id else []

    return get_all_or_none(sql, params)

def get_fines_last_updated() -> Optional[date]:
    sql = """
        SELECT value FROM metadata
        WHERE key = ?
    """

    params = ['last_update']

    result = get_one_or_none(sql, params)

    if not result:
        return None

    return date.fromisoformat(result[0])
