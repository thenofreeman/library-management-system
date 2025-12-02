#!/usr/bin/env python3

import argparse
from datetime import date
from typing import Optional
import database as db

from pprint import pprint

from database.common import Book, Fine
from database.query import book_available, get_borrower_by_id
from logger import Logger

def main() -> None:
    parser = argparse.ArgumentParser(description="Run the Library Management System.")
    parser.add_argument('-i', '--init', action='store_true', help='Specify to initialize the DB on startup.')
    parser.add_argument('-f', '--force', action='store_true', help='Force commands to execute (eg. force a re-init of the db).')
    parser.add_argument('-l', '--library', help='Pass a specific filename to be used for the database.')
    # parser.add_argument('-v', '--verbose', help='Show logs.')
    args = parser.parse_args()

    db_name = "library.db"

    if args.library:
        db_name = args.library

    db_exists = db.exists(db_name)

    if args.init:
        if db_exists:
            if args.force:
                print(f"Deleting the database at '{db_name}'.")
                db.delete(db_name)
            else:
                print(f"A database already exists at '{db_name}'. Either:")
                print(f"- Remove the init command line flag to use this database,")
                print(f"- Delete/Rename the file at '{db_name}', or")
                print(f"- Pass the force flag to override this error.")
                exit(1)

        print(f"Initializing the database.")
        db_exists = db.init(db_name)

        if db_exists:
            print(f"Database created and initialized at '{db_name}'.")
        else:
            print(f"Failed to initialize the database at '{db_name}'.")
            exit(1)

    if not db_exists:
        print("You must first initialize a database.")
        print("  Hint: Use the '--init' command line flag.")
        exit(1)

    milestone_2()

def start_application() -> None:
    pprint(search("will"))

def search(query: str) -> Optional[list[Book]]:
    return db.search_books(query)

def checkout(isbn: str, borrower_id: str) -> bool:
    borrower = db.get_borrower_by_id(borrower_id)

    if not borrower:
        Logger.error("Borrower doesn't exist.")
        return False

    checkouts = db.get_loans(borrower_id)

    if checkouts and len(checkouts) >= 3:
        Logger.error("Too many checkouts.")
        return False

    book = db.get_book(isbn)

    if not book:
        Logger.error("Book doesn't exist.")
        return False

    book_available = db.book_available(isbn)

    if not book_available:
        Logger.error("Book already checked out.")
        return False

    borrowers_fines = db.get_fines(borrower_id)

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

    fines = db.get_fines(borrower_id)

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

    books_out = db.get_fines(unpaid=True)

    if not books_out:
        # no books out, already up to date
        db.set_metadata_value('last_update', date.today().isoformat())
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
        db.set_metadata_value('last_update', date.today().isoformat())
        return True

    return False


#
#
#
# BELOW IS TEMPORARY CODE FOR MILESTONE 2 TESTING
# IT WILL BE REMOVED FOR MILESTONE 3
#
#
#


def milestone_2() -> None:
    while prompt_menu(): pass

def trunc(text, width):
    return text if len(text) <= width else text[:width-3] + "..."

def prompt_menu() -> bool:
    print("\n==== Menu ====")
    print("1. Book Search")
    print("2. Checkout Books")
    print("3. Checkin Books")
    print("4. Create Borrower")
    print("5. Enter Loan Payment")
    print("0. Quit")

    choice = input("\nMake a selection: ").strip()

    match choice:
        case "1": # book search
            query = input("\nSearch by Title, Author, or ISBN: ").strip()

            while not query:
                print("You must provide a search query.")
                query = input("\nSearch by Title, Author, or ISBN: ").strip()

            print(f"Searching for: {query}")

            results = search(query)

            if not results:
                print("No results from your query.")
            else:
                print(f"\n{'NO':<2} {'ISBN':<12} {'TITLE':<40} {'AUTHORS':<35} {'STATUS':<6}")

                for i, (isbn, title, authors, status) in enumerate(results, start=1):
                    print(f"{i:02d} {isbn:<12} {trunc(title, 40):<40} {trunc(authors, 35):<35} {'IN' if status else 'OUT':<6}")

        case "2": # check-out books
            borrower_id = input("\nEnter a Borrower Id: ").strip()

            while not borrower_id:
                print("You must provide a borrower ID.")
                borrower_id = input("\nEnter a Borrower Id: ").strip()

            isbn = input("Enter an ISBN: ").strip()

            while not isbn:
                print("You must provide an ISBN.")
                isbn = input("Enter an ISBN: ").strip()

            success = checkout(isbn, borrower_id)

            if not success:
                print("Failure checking out book")
            else:
                print("\nBook checked-out successfully.")

        case "3": # check-in books
            print("To search for a book, provide a value for at least one of the 3 fields.")
            print("Press enter to skip a field.")

            isbn = input("\nEnter an ISBN (optional): ").strip()
            borrower_id = input("Enter a Borrower Id (optional): ").strip()
            borrower_name = input("Enter a Borrower Name (optional): ").strip()

            while not (isbn or borrower_id or borrower_name):
                print("\nYou MUST provide a value to at least one of the 3 fields.")

                isbn = input("\nEnter an ISBN (optional): ").strip()
                borrower_id = input("Enter a Borrower Id (optional): ").strip()
                borrower_name = input("Enter a Borrower Name (optional): ").strip()

            checkouts = db.search_checkouts(isbn, borrower_id, borrower_name)

            if not checkouts:
                print("Nothing to checkin")
            else:
                print("Matching checkouts:")
                for i, (loan_id, isbn, title, borrower_id, borrower_name, _, _) in enumerate(checkouts, start=1):
                    print(f"\n{i}: LOAN ID: {loan_id}")
                    print(f"\tISBN: {isbn}")
                    print(f"\tTITLE: {trunc(title, 60)}")
                    print(f"\tBORROWER: {borrower_name} ({borrower_id})")

                while True:
                    print()
                    print("Select with books to checkin (max 3).")
                    print("Specify which numbers, separeted by spaces.")

                    sel_str = input("Selections (0 to cancel): ").strip()

                    try:
                        selections = [int(x) for x in sel_str.split(' ')]

                        break
                    except ValueError:
                        print("Not a valid selection.")

                if 0 in selections:
                    print("Cancelling operation.")
                else:
                    success = True

                    for checked_out in [checkouts[i-1] for i in selections]:
                        success = success and checkin(checked_out[0])

                    if not success:
                        print("Failure checking in book")
                    else:
                        print("\nBooks checked-in successfully.")

        case "4": # create borrower
            print()

            name = ""
            ssn = ""
            addr = ""

            while True:
                print("We need the following information to create a new borrower:")
                name = name or input("Borrower's Name: ").strip()
                ssn = ssn or input("Borrower's SSN: ").strip()
                addr = addr or input("Borrower's address: ").strip()

                if name and ssn and addr:
                    break
                else:
                    print("\nMissing information.")

            print("\nCreating a new borrower for:")
            print(f"Name: {name}")
            print(f"SSN: {ssn}")
            print(f"Address: {addr}")

            success = create_borrower(name, ssn, addr)

            borrower_id = db.get_borrower_by_ssn(ssn)

            if not success:
                print("Failure creating borrower")
            else:
                print(f"\nBorrower successfully created with ID: {borrower_id}.")

        case "5": # payment
            while True:
                borrower_id = input("Enter a Borrower Id: ").strip()

                if borrower_id:
                    break
                else:
                    print("\nYou must provide an Id.")

            amt_owed = db.get_fines(borrower_id)

            if amt_owed is None:
                print("Failure getting fines")
            elif amt_owed == 0:
                print(f"\n Borrower owes nothing.")
            else:
                print(f"\n Borrower owes: {amt_owed}")

                while True:
                    try:
                        amt_to_pay = int(float(input("Enter an amount to pay: ").strip()) * 100)

                        break
                    except ValueError:
                        print("\nPlease provide a number.")

                success = pay_fines(borrower_id, amt_to_pay)

                if not success:
                    print("Failure paying fines")
                else:
                    print(f"\nAll fines for {borrower_id} have been paid off.")

        case "0":
            print("\nQuitting...")
            return False

        case _:
            print("Invalid selection. Please try again.")

    return True

if __name__ == '__main__':
    main()
