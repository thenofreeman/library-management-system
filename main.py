#!/usr/bin/env python3

import sys

from common import BookSearchResult, trunc
from search import search
from initialize import init_db, reinit_db
from logger import logger

def checkout(isbn: str, borrower_id: str) -> None:
    pass

# def checkin(isbn: str, borrower_id: str) -> Result:
#     pass

def create_borrower(name: str, ssn: str, address: str) -> None:
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
                print("Search cancelled. No input provided.")
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
