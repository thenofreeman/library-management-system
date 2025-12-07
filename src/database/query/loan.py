from typing import Optional
from datetime import datetime, timedelta

from database.names import (
    BOOK_LOANS_TABLE_NAME,
)

from database.dtypes import Loan

from . import query

def search_loans(isbn: str | None = None,
                     borrower_id: str | None = None,
                     name: str | None = None,
                     only_returned: bool | None = None) -> Optional[list[Loan]]:
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
      {'' if only_returned else 'AND l.Date_in IS NULL'}
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

    return query.get_all_or_none(sql, params)

def get_loans_by_borrower_id(borrower_id: str, only_returned: bool = False) -> Optional[list[Loan]]:
    return search_loans(borrower_id=borrower_id, only_returned=only_returned)

def get_loans_by_isbn(isbn: str, only_returned: bool = False) -> Optional[list[Loan]]:
    return search_loans(isbn=isbn, only_returned=only_returned)

def create_loan(isbn: str, borrower_id: str) -> bool:
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
    due_date = datetime.today() + timedelta(days=14)

    params = [isbn, borrower_id, date_out, due_date]

    return query.try_execute_one(sql, params)

def resolve_loan(loan_id: int) -> bool:
    sql = f"""
        UPDATE {BOOK_LOANS_TABLE_NAME}
        SET Date_in = ?
        WHERE Loan_id = ?
    """

    date_in = datetime.now().strftime('%Y-%m-%d')

    params = [date_in, loan_id]

    return query.try_execute_one(sql, params)
