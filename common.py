
DB_NAME = "library.db"

BOOK_TABLE = 'BOOK'
BOOK_AUTHORS_TABLE = 'BOOK_AUTHORS'
AUTHORS_TABLE = 'AUTHORS'
BORROWER_TABLE = 'BORROWER'
BOOK_LOANS_TABLE = 'BOOK_LOANS'
FINES_TABLE = 'FINES'

def trunc(text, width):
    return text if len(text) <= width else text[:width-3] + "..."

# isbn, title, authors, status
type BookSearchResult = tuple[str, str, list[str], bool]
# loan_id, isbn, title, borrower_id, borrower_name
type BorrowerSearchResult = tuple[str, str, str, str, str]
