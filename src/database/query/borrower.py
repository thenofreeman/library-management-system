from typing import Optional

from models import BorrowerSearchResult, Borrower

from database.names import (
    BOOK_LOANS_TABLE_NAME,
    BORROWERS_TABLE_NAME,
    FINES_TABLE_NAME
)

import database as db

from . import query

from logger import Logger

def search_borrowers(search_term: str) -> list[BorrowerSearchResult]:
    if not search_term:
        return []

    sql = f"""
        SELECT
            b.Card_id,
            b.Bname,
            COUNT(
                DISTINCT CASE
                    WHEN l.Date_in IS NULL
                    THEN l.Loan_id
                END
            ) as N_Active_loans,
            COALESCE(SUM(
                CASE
                    WHEN l.Date_in IS NULL
                    THEN f.Fine_amt - f.Paid
                    ELSE 0
                END
            ), 0) as Outstanding_fines
        FROM {BORROWERS_TABLE_NAME} b
        LEFT JOIN {BOOK_LOANS_TABLE_NAME} l ON b.Card_id = l.Card_id
        LEFT JOIN {FINES_TABLE_NAME} f ON l.Loan_id = f.Loan_id
        WHERE LOWER(b.Bname) LIKE LOWER(?)
           OR CAST(b.Card_id AS TEXT) LIKE ?
        GROUP BY b.Card_id, b.Bname
        ORDER BY b.Card_id;
    """

    params = [f"%{search_term}%" for _ in range(2)]

    results = query.get_all_or_none(sql, params)

    if not results:
        return []

    return [BorrowerSearchResult(**dict(result)) for result in results]

def get_borrower_by_ssn(ssn: str) -> Optional[Borrower]:
    return _get_borrower("Ssn", ssn)

def get_borrower_by_id(borrower_id: int) -> Optional[Borrower]:
    return _get_borrower("Card_id", str(borrower_id))

def _get_borrower(column: str, param: str) -> Optional[Borrower]:
    if column == 'Card_id':
        column = 'b.Card_id'

    sql = f"""
    SELECT
        b.Card_id,
        b.Ssn,
        b.Bname,
        b.Address,
        b.Phone
    FROM {BORROWERS_TABLE_NAME} b
    WHERE {column} = ?
    """

    result = query.get_one_or_none(sql, [param])

    if not result:
        return None

    return Borrower(**dict(result))

def create_borrower(name: str, ssn: str, address: str) -> bool:
    borrower = db.get_borrower_by_ssn(ssn)

    if borrower:
        Logger.error("Borrower already exists.")
        return False

    sql = f"""
    INSERT INTO {BORROWERS_TABLE_NAME} (
        Bname,
        Ssn,
        Address
    ) VALUES (?, ?, ?)
    """

    params = [name, ssn, address]

    return query.try_execute_one(sql, params)
