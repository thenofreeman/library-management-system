import os
import sqlite3
from pathlib import Path

from logger import logger
from common import AUTHORS_TABLE, BOOK_AUTHORS_TABLE, BOOK_LOANS_TABLE, BOOK_TABLE, BORROWER_TABLE, DB_NAME, FINES_TABLE
from normalize import read_books, read_borrowers
import database as db

def create_database(filename: str) -> None:
    if Path(filename).is_file():
        logger.write(f"Unable to initialize. DB file '{filename}' already exists.")
        logger.write("Rename or delete the file and try again.")

        logger.setError()
        return

    create_books_table = f"""
        CREATE TABLE {BOOK_TABLE} (
            Isbn TEXT NOT NULL,
            Title TEXT NOT NULL,

            PRIMARY KEY (Isbn)
        );
    """

    create_book_authors_table = f"""
        CREATE TABLE {BOOK_AUTHORS_TABLE} (
            Author_id TEXT NOT NULL,
            Isbn TEXT NOT NULL,

            PRIMARY KEY(Author_id, Isbn),

            FOREIGN KEY(Author_id) REFERENCES AUTHORS(Author_id),
            FOREIGN KEY(Isbn) REFERENCES BOOK(Isbn)
        );
    """

    create_authors_table = f"""
        CREATE TABLE {AUTHORS_TABLE} (
            Author_id TEXT NOT NULL,
            Name TEXT NOT NULL,

            PRIMARY KEY (Author_id)
        );
    """

    create_borrower_table = f"""
        CREATE TABLE {BORROWER_TABLE} (
            Card_id TEXT NOT NULL,
            Ssn TEXT NOT NULL,
            Bname TEXT NOT NULL,
            Address TEXT NOT NULL,
            Phone TEXT NOT NULL,

            PRIMARY KEY (Card_id)
        );
    """

    create_book_loans_table = f"""
        CREATE TABLE {BOOK_LOANS_TABLE} (
            Loan_id TEXT NOT NULL,
            Isbn TEXT NOT NULL,
            Card_id TEXT NOT NULL,
            Date_out TEXT NOT NULL,
            Date_in TEXT,

            PRIMARY KEY (Loan_id),

            FOREIGN KEY(Isbn) REFERENCES BOOK(Isbn),
            FOREIGN KEY(Card_id) REFERENCES BORROWER(Card_id)
        );
    """

    create_fines_table = f"""
        CREATE TABLE {FINES_TABLE} (
            Loan_id TEXT NOT NULL,
            Fine_amt TEXT NOT NULL,
            Paid INTEGER NOT NULL,

            PRIMARY KEY (Loan_id),

            FOREIGN KEY(Loan_id) REFERENCES BOOK_LOANS(Loan_id)
        );
    """

    logger.write(f"Creating DB file '{filename}'...")

    conn = sqlite3.connect(filename)
    c = conn.cursor()

    logger.write("Creating tables...\n")

    c.execute(create_books_table)
    c.execute(create_book_authors_table)
    c.execute(create_authors_table)
    c.execute(create_borrower_table)
    c.execute(create_book_loans_table)
    c.execute(create_fines_table)

    logger.write("Tables created.")
    logger.write()

    conn.close()

    logger.write(f"Database successfully created at {filename}.")

def write_to_db(db_filename: str, data: list[list[str]], table_name: str) -> None:
    conn = sqlite3.connect(db_filename)
    c = conn.cursor()

    print(data[0])
    print(data[1])
    print()
    print()

    conn.close()

def init_db() -> None:
    # TODO: err checking on this file
    borrowers = read_borrowers()
    # TODO: err checking on this file
    (books, book_authors, authors) = read_books()

    create_database(DB_NAME)

    if logger.hasErrored():
        return

    db.write_books(books)
    db.write_book_authors(book_authors)
    db.write_authors(authors)
    db.write_borrowers(borrowers)

def reinit_db() -> None:
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
        logger.write(f"Previous db '{DB_NAME}' removed.")
    else:
        logger.write(f"No previous db '{DB_NAME}' found.")

    init_db()
