from datetime import date
from typing import Optional

import database as db

from database.dtypes import Book
from logger import Logger

def search(query: str) -> Optional[list[Book]]:
    return db.search_books(query)

def checkout(isbn: str, borrower_id: str) -> bool:
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

    return db.create_loan(isbn, borrower_id)

def checkin(loan_id: int) -> bool:
    return db.resolve_loan(loan_id)

def create_borrower(name: str, ssn: str, address: str) -> bool:
    borrower = db.get_borrower_by_ssn(ssn)

    if borrower:
        Logger.error("Borrower already exists.")
        return False

    return db.create_borrower(name, ssn, address)

def pay_fines(borrower_id: str, amt: int) -> bool:
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

    success = db.update_fines(fines_to_update)

    if success:
        db.set_fines_updated(date.today().isoformat())
        return True

    return False
