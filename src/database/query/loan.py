from typing import Optional
from datetime import datetime, timedelta

from database.names import (
    BOOK_LOANS_TABLE_NAME,
)

from models import Loan

import database as db

from . import query

from logger import Logger

def search_loans(isbn: str | None = None,
                 borrower_id: str | None = None,
                 name: str | None = None,
                 returned: bool = False) -> list[Loan]:
    sql = f"""
    SELECT
        l.Loan_id,
        l.Isbn,
        l.Card_id,
        b.Title,
        l.Date_out,
        l.Due_date,
        l.Date_in
    FROM BOOK_LOANS l
    JOIN BOOK b ON b.Isbn = l.Isbn
    JOIN BORROWER br ON br.Card_id = l.Card_id
    """

    conditions = []
    params = []

    if not returned:
        sql += ' WHERE l.Date_in IS NULL'

    if isbn:
        conditions.append("l.Isbn LIKE ? COLLATE NOCASE")
        params.append(f"%{isbn}%")

    if borrower_id:
        conditions.append("br.Card_id LIKE ?")
        params.append(f"%{borrower_id}%")

    if name:
        conditions.append("br.Bname LIKE ? COLLATE NOCASE")
        params.append(f"%{name}%")

    if conditions:
        if returned:
            sql += " WHERE (" + " OR ".join(conditions) + ")"
        else:
            sql += " AND (" + " OR ".join(conditions) + ")"

    sql += " ORDER BY l.Date_out DESC"

    results = query.get_all_or_none(sql, params)

    if not results:
        return []

    return [Loan(**dict(result)) for result in results]

def get_all_loans(overdue: bool = False, returned: bool = False) -> list[Loan]:
    return [loan for loan in db.search_loans(returned=returned) if not overdue or loan.is_overdue]

def get_loans_by_borrower_id(borrower_id: int, returned: bool = False) -> list[Loan]:
    return db.search_loans(borrower_id=str(borrower_id), returned=returned)

def get_loans_by_isbn(isbn: str, returned: bool = False) -> list[Loan]:
    return db.search_loans(isbn=isbn, returned=returned)

def checkout(isbn: str, borrower_id: int) -> bool:
    return db.create_loan(isbn, borrower_id)

def create_loan(isbn: str, borrower_id: int) -> bool:
    borrower = db.get_borrower_by_id(borrower_id)

    if not borrower:
        Logger.error("Borrower doesn't exist.")
        return False

    checkouts = db.get_loans_by_borrower_id(borrower_id)

    if checkouts and len(checkouts) >= 3:
        Logger.error("Too many checkouts.")
        return False

    book = db.get_book_by_isbn(isbn)

    if not book:
        Logger.error("Book doesn't exist.")
        return False

    book_available = db.book_available_with_isbn(isbn)

    if not book_available:
        Logger.error("Book already checked out.")
        return False

    borrowers_fines = db.get_fines_by_borrower_id(borrower_id)

    if borrowers_fines and len(borrowers_fines) > 0:
        Logger.error("Borrower has pending fines.")
        return False

    sql = f"""
    INSERT INTO {BOOK_LOANS_TABLE_NAME} (
        Isbn,
        Card_id,
        Date_out,
        Due_date,
        Date_in
    ) VALUES (?, ?, ?, ?, NULL)
    """

    date_out = datetime.now().strftime('%Y-%m-%d')
    due_date = (datetime.today() + timedelta(days=14)).strftime('%Y-%m-%d')

    params = [isbn, borrower_id, date_out, due_date]

    return query.try_execute_one(sql, params)

def checkin_many(loans: list[Loan]) -> bool:
    all_success = True

    for loan in loans:
        success = db.checkin(loan.id)

        all_success = all_success and success

    return all_success

def checkin(loan_id: int) -> bool:
    return db.resolve_loan(loan_id)

def resolve_loan(loan_id: int) -> bool:
    sql = f"""
        UPDATE {BOOK_LOANS_TABLE_NAME}
        SET Date_in = ?
        WHERE Loan_id = ?
    """

    date_in = db.get_current_date()

    params = [date_in, loan_id]

    return query.try_execute_one(sql, params)
