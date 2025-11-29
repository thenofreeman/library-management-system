#!/usr/bin/env python3

import sys
import os

from common import trunc, DB_NAME
from db.query import get_borrower_id
from operations import create_borrower, search, checkout, checkin, init_db, reinit_db
from logger import logger

import db

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

    if not os.path.isfile(DB_NAME):
        logger.errorAll([
            f"No database found for '{DB_NAME}'",
            f"Run init command as per README"
        ])

    if logger.hasErrored():
        print(logger.flush())
        sys.exit(1)

    if not logger.empty():
        print(logger.flush())

    while prompt_menu(): pass

def prompt_menu() -> bool:
    print("\n==== Menu ====")
    print("1. Book Search")
    print("2. Checkout Books")
    print("3. Checkin Books")
    print("4. Create Borrower")
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
                print(logger.flush())
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
                print(logger.flush())
            else:
                print("Matching checkouts:")
                for i, (loan_id, isbn, title, borrower_id, borrower_name) in enumerate(checkouts, start=1):
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
                        print(logger.flush())
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

            borrower_id = get_borrower_id(ssn)

            if not success:
                print(logger.flush())
            else:
                print(f"\nBorrower successfully created with ID: {borrower_id}.")

        case "0":
            print("\nQuitting...")
            return False

        case _:
            print("Invalid selection. Please try again.")

    return True

if __name__ == '__main__':
    main()
