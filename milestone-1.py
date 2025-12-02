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
                print("Borrower has no pending fines")
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
