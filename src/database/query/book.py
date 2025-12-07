from typing import Optional

from database.dtypes import Book
from database.names import (
    BOOKS_TABLE_NAME,
    BOOK_AUTHORS_TABLE_NAME,
    BOOK_LOANS_TABLE_NAME,
    AUTHORS_TABLE_NAME,
    BORROWERS_TABLE_NAME
)

from . import query

def search_books(search_term: str) -> Optional[list[Book]]:
    if not search_term:
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
        END as Status,
        br.Card_id
    FROM {BOOKS_TABLE_NAME} b
    LEFT JOIN {BOOK_AUTHORS_TABLE_NAME} ba ON ba.Isbn = b.Isbn
    LEFT JOIN {AUTHORS_TABLE_NAME} a ON a.Author_id = ba.Author_id
    LEFT JOIN {BOOK_LOANS_TABLE_NAME} l ON b.Isbn = l.Isbn
    LEFT JOIN {BORROWERS_TABLE_NAME} br ON br.Card_id = l.Card_id
    WHERE b.Isbn LIKE ? COLLATE NOCASE
       OR b.Title LIKE ? COLLATE NOCASE
       OR a.Name LIKE ? COLLATE NOCASE
    GROUP BY b.Isbn, b.Title, l.Isbn, l.Date_in
    """
    params = [f"%{search_term}%" for _ in range(3)]

    return query.get_all_or_none(sql, params)

def get_book_by_isbn(isbn: str) -> Optional[Book]:
    books = search_books(isbn)

    if not books:
        return None

    return books[0]

def book_exists_with_isbn(isbn: str) -> bool:
    return get_book_by_isbn(isbn) is not None

def book_available_with_isbn(isbn: str) -> bool:
    sql = f"""
    SELECT
        COUNT(*) as n_checkouts
    FROM {BOOK_LOANS_TABLE_NAME}
    WHERE Isbn = ?
      AND Date_in IS NULL
    """

    result = query.get_one_or_none(sql, [isbn])

    if result is None:
        return True

    return result[0] == 0
