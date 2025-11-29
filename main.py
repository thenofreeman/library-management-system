#!/usr/bin/env python3

import sys

from common import BookSearchResult, trunc
from operations import search, checkout, checkin, init_db, reinit_db
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

    if not logger.empty():
        print(logger.flush())

    while prompt_menu(): pass

def prompt_menu() -> bool:
    print("\n==== Menu ====")
    print("1. Book Search")
    print("2. Checkout Books")
    print("3. Checkin Books")
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
            borrower_id = input("\nEnter a Borrower Id: ").strip()

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
        case "3":
            isbn = input("\nEnter an ISBN: ").strip()
            borrower_id = input("Enter a Borrower Id: ").strip()
            borrower_name = input("Enter a Borrower Name: ").strip()

            checkouts = db.search_checkouts(isbn, borrower_id, borrower_name)

            if logger.hasErrored():
                print(logger.flush())
            else:
                if checkouts:
                    print(checkouts)
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
