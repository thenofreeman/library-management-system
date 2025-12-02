from datetime import date

# constants

BOOKS_TABLE_NAME = 'BOOK'
BOOK_AUTHORS_TABLE_NAME = 'BOOK_AUTHORS'
AUTHORS_TABLE_NAME = 'AUTHORS'
BORROWERS_TABLE_NAME = 'BORROWER'
BOOK_LOANS_TABLE_NAME = 'BOOK_LOANS'
FINES_TABLE_NAME = 'FINES'
METADATA_TABLE_NAME = 'metadata'

# types

type StringMatrix = list[list[str]]
type CSVData = tuple[StringMatrix, StringMatrix, StringMatrix, StringMatrix]

type Book = tuple[str, str, str, bool] # isbn, title, authors, status
type Author = tuple[str, str] # id, name
type Borrower = tuple[int, str, str, str, str] # borrower_id, ssn, name, addr, phone
type Loan = tuple[int, str, str, int, str, date, date] # id, isbn, title, borrower_id, name, date_o, date_i
type Fine = tuple[int, int, str, bool, date, date] # id, amt, isbn, paid, date_o, date_i
