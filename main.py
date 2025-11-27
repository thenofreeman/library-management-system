#!/usr/bin/env python3

import os
import sqlite3
import sys
import uuid
from datetime import datetime

from common import BOOK_LOANS_TABLE, BOOK_TABLE, DB_NAME, FINES_TABLE, BookSearchResult, trunc
from search import search
from initialize import init_db, reinit_db
from logger import logger

def checkout(isbn: str, borrower_id: str) -> None:
    if not os.path.isfile(DB_NAME):
        logger.errorAll([
            f"No database found for '{DB_NAME}'",
            f"Run init command as per README"
        ])

        return

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # check if borrower has more than 3 active checkouts and deny if true
    sql = f"""
    SELECT
        b.Isbn,
        b.Title,
        l.Date_out,
        l.Date_in,
        l.Loan_id
    FROM {BOOK_TABLE} b
    JOIN {BOOK_LOANS_TABLE} l ON l.Isbn = b.Isbn
    WHERE l.Card_id = ?
      AND l.Date_in IS NULL
    """

    c.execute(sql, [borrower_id])
    checkouts = c.fetchall()

    if len(checkouts) > 3:
        logger.error(f"Max checkouts is 3. Borrower has {len(checkouts)}")

    # check if book is already checked out
    sql = f"""
    SELECT
        COUNT(*) as n_checkouts
    FROM {BOOK_LOANS_TABLE}
    WHERE Isbn = ?
      AND Date_in IS NULL
    """

    c.execute(sql, [isbn])
    is_checked_out = c.fetchone()[0]

    if is_checked_out > 0: # its stored as integer in sqlite
        logger.error(f"The requested book is already checked out.")

    # check unpaid fines and deny checkout
    sql = f"""
    SELECT
        f.Loan_id,
        f.Fine_amt,
        f.Paid,
        b.Title,
        b.Isbn,
        l.Date_out
    FROM {FINES_TABLE} f
    JOIN {BOOK_LOANS_TABLE} l ON l.Loan_id = f.Loan_id
    JOIN {BOOK_TABLE} b ON b.Isbn = l.Isbn
    WHERE f.Paid = 0
      AND l.Card_id = ?
    ORDER BY l.Date_out DESC
    """

    c.execute(sql, [borrower_id])
    borrower_fines = c.fetchall()

    if len(borrower_fines) > 0:
        logger.error(f"Borrower has pending fines:")
        for (_, amt, _, isbn, title, date_out) in borrower_fines:
            logger.error(f"{isbn:<12} {title:<35} {amt} {date_out}")

    generated_loan_id = str(uuid.uuid4())
    date_out = datetime.now().strftime('%Y-%m-%d')

    sql = f"""
    INSERT INTO {BOOK_LOANS_TABLE} (
        Loan_id,
        Isbn,
        Card_id,
        Date_out,
        Date_in
    ) VALUES (?, ?, ?, ?, NULL)
    """

    try:
        c.execute(sql, [generated_loan_id, isbn, borrower_id, date_out])
        conn.commit()
    except sqlite3.Error as e:
        logger.error(e.__str__())

        conn.rollback()

    conn.close()

def checkin(isbn: str, borrower_id: str) -> None:
    # locate books based on isbn, card_no and/or bname
    # provide a way of selecting up to 3 books to checkin
    pass

def create_borrower(name: str, ssn: str, address: str) -> None:
    # all params required.. phone?
    # generate new card id that is compatible with existing ids
    # ensure only one borrower per ssn is created
    pass

# fines..
#

def main() -> None:
    nargs = len(sys.argv)

    if nargs > 2:
        print("Too many arguments given")
        print("Quitting..")
        sys.exit(1)
    elif nargs == 2:
        if sys.argv[1] == "--init":
            init_db()
        elif sys.argv[1] == "--reinit":
            reinit_db()
        else:
            print(f"Invalid command line argument: '{sys.argv[1]}'")
            print("Quitting..")
            sys.exit(1)
    else:
        pass # no arguments given

    if not logger.empty():
        print(logger.flush())

    while prompt_menu(): pass

def prompt_menu() -> bool:
    print("\n==== Menu ====")
    print("1. Book Search")
    print("2. Checkout Books")
    print("0. Quit")

    choice = input("\nMake a selection: ").strip()

    match choice:
        case "1":
            query = input("\nSearch by Title, Author, or ISBN: ").strip()

            if query:
                print(f"Searching for: {query}")

                results = search(query)

                if logger.hasErrored():
                    print(logger.flush())
                else:
                    if results:
                        print_books(results)
            else:
                print("Operation cancelled. You must provide a search query.")
        case "2":
            borrower_id = input("Enter a Borrower Id: ").strip()

            if borrower_id:
                isbn = input("Enter an ISBN: ").strip()

                if isbn:
                    checkout(isbn, borrower_id)

                    if logger.hasErrored():
                        print(logger.flush())
                    else:
                        print("Book checked-out successfully.")
                else:
                    print("Operation cancelled. You must provide an ISBN.")
            else:
                print("Operation cancelled. You must provide a borrower ID.")

        case "0":
            print("\nQuitting...")
            return False
        case _:
            print("Invalid selection. Please try again.")

    return True

def print_books(books: list[BookSearchResult]):
    print(f"\n{'NO':<2} {'ISBN':<12} {'TITLE':<40} {'AUTHORS':<35} {'STATUS':<6}")

    for i, (isbn, title, authors, status) in enumerate(books, start=1):
        print(f"{i:02d} {isbn:<12} {trunc(title, 40):<40} {trunc(authors, 35):<35} {'IN' if status else 'OUT':<6}")

if __name__ == '__main__':
    main()
