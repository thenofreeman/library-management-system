from typing import Optional

from database.dtypes import Borrower
from database.names import (
    BOOKS_TABLE_NAME,
    BOOK_AUTHORS_TABLE_NAME,
    BOOK_LOANS_TABLE_NAME,
    AUTHORS_TABLE_NAME,
    BORROWERS_TABLE_NAME
)

from . import query

# TODO: NOT PROPER QUERY
def search_borrowers(search_term: str) -> Optional[list[Borrower]]:
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
        br.
    FROM {BOOKS_TABLE_NAME} b
    LEFT JOIN {BOOK_AUTHORS_TABLE_NAME} ba ON ba.Isbn = b.Isbn
    LEFT JOIN {AUTHORS_TABLE_NAME} a ON a.Author_id = ba.Author_id
    LEFT JOIN {BOOK_LOANS_TABLE_NAME} l ON b.Isbn = l.Isbn
    WHERE b.Isbn LIKE ? COLLATE NOCASE
       OR b.Title LIKE ? COLLATE NOCASE
       OR a.Name LIKE ? COLLATE NOCASE
    GROUP BY b.Isbn, b.Title, l.Isbn, l.Date_in
    """
    params = [f"%{search_term}%" for _ in range(3)]

    return query.get_all_or_none(sql, params)

def get_borrower_by_ssn(ssn: str) -> Optional[Borrower]:
    return _get_borrower("Ssn", ssn)

def get_borrower_by_id(borrower_id: str) -> Optional[Borrower]:
    return _get_borrower("Card_id", borrower_id)

def _get_borrower(column: str, param: str) -> Optional[Borrower]:
    sql = f"""
    SELECT
        Card_id,
        Ssn,
        Bname,
        Address,
        Phone
    FROM {BORROWERS_TABLE_NAME}
    WHERE {column} = ?
    """

    return query.get_one_or_none(sql, [param])

def create_borrower(name: str, ssn: str, address: str) -> bool:
    sql = f"""
    INSERT INTO {BORROWERS_TABLE_NAME} (
        Bname,
        Ssn,
        Address
    ) VALUES (?, ?, ?)
    """

    params = [name, ssn, address]

    return query.try_execute_one(sql, params)
