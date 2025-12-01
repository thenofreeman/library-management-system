import os
from pathlib import Path
from datetime import date

import db
from logger import logger
from common import DB_NAME, BookSearchResult, BorrowerSearchResult

def init_db() -> None:
    if Path(DB_NAME).is_file():
        logger.error(f"Unable to initialize. DB file '{DB_NAME}' already exists.")
        logger.error("Rename or delete the file and try again.")

        return

    # TODO: err checking on this file
    borrowers = db.read_borrowers()
    # TODO: err checking on this file
    (books, book_authors, authors) = db.read_books()

    db.create_database()

    if logger.hasErrored():
        return

    db.init_books(books)
    db.init_book_authors(book_authors)
    db.init_authors(authors)
    db.init_borrowers(borrowers)

def reinit_db() -> None:
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
        logger.write(f"Previous db '{DB_NAME}' removed.")
    else:
        logger.write(f"No previous db '{DB_NAME}' found.")

    init_db()

def search(query: str) -> list[BookSearchResult]:
    return db.search_books(query)

def checkout(isbn: str, borrower_id: str) -> bool:
    checkouts = db.get_checkouts(borrower_id)

    if len(checkouts) >= 3:
        logger.error(f"Max checkouts is 3. Borrower has {len(checkouts)}")

    exists = db.book_exists(isbn)

    if not exists:
        logger.error(f"The requested book does not exist in the database.")

    checked_out = db.is_available(isbn)

    if checked_out:
        logger.error(f"The requested book is already checked out.")

    borrower_fines = db.get_fines(borrower_id)

    if len(borrower_fines) > 0:
        logger.error(f"Borrower has pending fines:")
        for (_, amt, _, isbn, title, date_out) in borrower_fines:
            logger.error(f"{isbn:<12} {title:<35} {amt} {date_out}")

    if logger.hasErrored():
        return False

    return db.create_loan(isbn, borrower_id)

def checkin(loan_id: str) -> bool:
    return db.resolve_loan(loan_id)

def create_borrower(name: str, ssn: str, address: str) -> bool:
    exists = db.borrower_exists(ssn)

    if exists:
        logger.error("Cannot create borrower. A borrower with this SSN already exists.")

        return False

    return db.create_borrower(name, ssn, address)

def update_fines() -> bool:

    last_update = db.last_updated_fines()
    today = date.today()

    should_update = (last_update is None) or (last_update >= today)

    if not should_update:
        return True

    books_out = db.get_checkouts()

    fines = []

    for book in books_out:

        loan_id = book[4]

        start_date = book[2]
        end_date = book[3] if book[3] else today

        fine_amt = (start_date - end_date) * 0.25

        fines.append((loan_id, fine_amt))

    success = db.update_fines(fines)

    db.set_metadata_value('last_update', date.today().isoformat())

    return success

def get_fines(borrower_id: str) -> int | None:
    if not db.borrower_id_exists(borrower_id):
        logger.error(f"Borrower with id '{borrower_id}' does not exist.")

        return None

    fines = db.get_fines(borrower_id)
    total_fines = sum(fine[1] for fine in fines)

    return total_fines

def pay_fines(borrower_id: str, amt: int) -> bool:
    if not db.borrower_id_exists(borrower_id):
        logger.error(f"Borrower with id '{borrower_id}' does not exist.")

        return False

    fines = db.get_fines(borrower_id)
    total_fines = sum(fine[1] for fine in fines)

    if amt < total_fines:
        logger.error(f"Amount paid is less than total fines owed.")

        return False

    loan_ids = [fine[0] for fine in fines]

    return db.pay_fines(loan_ids)
