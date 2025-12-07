from typing import Optional
from datetime import date

from database.dtypes import Fine
from database.names import (
    FINES_TABLE_NAME,
    BOOK_LOANS_TABLE_NAME,
    BOOKS_TABLE_NAME
)

from . import query, metadata

def get_all_fines(unpaid: bool = False) -> Optional[list[Fine]]:
    sql = f"""
    SELECT
        f.Loan_id,
        f.Fine_amt,
        b.Isbn,
        f.Paid
    FROM {FINES_TABLE_NAME} f
    JOIN {BOOK_LOANS_TABLE_NAME} l ON l.Loan_id = f.Loan_id
    JOIN {BOOKS_TABLE_NAME} b ON b.Isbn = l.Isbn
    {'WHERE f.Paid = 0' if unpaid else ''}
    ORDER BY l.Date_out DESC
    """

    return query.get_all_or_none(sql, [])

def get_fines_by_borrower_id(borrower_id: str, unpaid: bool = False) -> Optional[list[Fine]]:
    sql = f"""
    SELECT
        f.Loan_id,
        f.Fine_amt,
        b.Isbn,
        f.Paid
    FROM {FINES_TABLE_NAME} f
    JOIN {BOOK_LOANS_TABLE_NAME} l ON l.Loan_id = f.Loan_id
    JOIN {BOOKS_TABLE_NAME} b ON b.Isbn = l.Isbn
    WHERE l.Card_id = ? {'AND f.Paid = 0' if unpaid else ''}
    ORDER BY l.Date_out DESC
    """

    params = [borrower_id] if borrower_id else []

    return query.get_all_or_none(sql, params)

def set_fines_updated(date_str: str) -> bool:
    return metadata.set_value('last_updated_fines', date_str)

def get_fines_last_updated() -> Optional[date]:
    result = metadata.get_value('last_updated_fines')

    if not result:
        return None

    return result.fromisoformat(result[0])

def update_fines(fines: list[tuple]) -> bool:
    sql = f"""
        UPDATE {FINES_TABLE_NAME}
        SET Fine_amt = ?
        WHERE Loan_id = ?
    """

    if not fines:
        return True

    (fines, loan_ids) = tuple(map(list, zip(*fines)))

    params = [(fines, loan_ids, )]

    return query.try_execute_many(sql, params)

def resolve_fines(loan_ids: list[int]) -> bool:
    sql = f"""
        UPDATE {FINES_TABLE_NAME}
        SET Paid = 1
        WHERE Loan_id = ?
    """

    params = [(loan_id,) for loan_id in loan_ids]

    return query.try_execute_many(sql, params)
