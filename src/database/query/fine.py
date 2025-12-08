from typing import Optional
from datetime import date, datetime

from database.dtypes import Fine
from database.names import (
    FINES_TABLE_NAME,
    BOOK_LOANS_TABLE_NAME,
    BOOKS_TABLE_NAME
)

import database as db

from . import query, metadata

from logger import Logger

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

def get_fines_by_borrower_id(borrower_id: int, unpaid: bool = False) -> Optional[list[Fine]]:
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

    return datetime.fromisoformat(result[0])

def pay_fines(borrower_id: int, amt: int) -> bool:
    borrower = db.get_borrower_by_id(borrower_id)

    if not borrower:
        Logger.error("Borrower doesn't exist.")
        return False

    fines = db.get_fines_by_borrower_id(borrower_id)

    if not fines:
        # no fines to pay
        return True

    total_fines = sum(fine[1] for fine in fines)

    if amt < total_fines:
        Logger.error("Borrower didn't pay enough fine.")
        return False

    loan_ids = [fine[0] for fine in fines]

    return db.resolve_fines(loan_ids)

def resolve_fines(loan_ids: list[int]) -> bool:
    sql = f"""
        UPDATE {FINES_TABLE_NAME}
        SET Paid = 1
        WHERE Loan_id = ?
    """

    params = [(loan_id,) for loan_id in loan_ids]

    return query.try_execute_many(sql, params)

def update_fines() -> bool:
    last_update = db.get_fines_last_updated()
    today = date.today()

    should_update = (last_update is None) or (last_update >= today)

    if not should_update:
        return True

    books_out = db.get_all_fines(unpaid=True)

    if not books_out:
        # no books out, already up to date
        db.set_fines_updated(date.today().isoformat())
        return True

    fines_to_update = []

    for book in books_out:
        start_date = book[4]
        end_date = book[5] if book[5] else today

        loan_id = book[4]
        fine_amt = (start_date - end_date) * 0.25

        fines_to_update.append((loan_id, fine_amt))

    success = db.set_fines(fines_to_update)

    if success:
        db.set_fines_updated(date.today().isoformat())
        return True

    return False

def set_fines(fines: list[tuple]) -> bool:
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
