import os
from pathlib import Path

import db
from logger import logger
from common import DB_NAME, BookSearchResult

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

    if exists:
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

def checkin(isbn: str, borrower_id: str) -> None:
    # provide a way of selecting up to 3 books to checkin
    pass

def create_borrower(name: str, ssn: str, address: str) -> None:
    # all params required.. phone?
    # generate new card id that is compatible with existing ids
    # ensure only one borrower per ssn is created
    pass

# fines..
#
