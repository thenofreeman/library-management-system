from datetime import date
from typing import Optional

type StringMatrix = list[list[str]]
type CSVData = tuple[StringMatrix, StringMatrix, StringMatrix, StringMatrix]

type Book = tuple[Isbn, Title, Authors, Status]
type Author = tuple[AuthorId, FullName]
type Borrower = tuple[BorrowerId, Ssn, FullName, Address, Phone]
type Loan = tuple[LoanId, Isbn, Title, BorrowerId, DateOut, DueDate, DateIn]
type Fine = tuple[FineId, Cents, Isbn, IsPaid, DateOut, DateIn]

type BookSearchResult = tuple[Isbn, Title, Authors, Status, Optional[BorrowerId]]
type BorrowerSearchResult = tuple[BorrowerId, FullName, ActiveLoanCount, TotalUnpaidFines]
type LoanSearchResult = tuple[LoanId, Isbn, Title, BorrowerId, DateOut, DueDate, DateIn]

# NOTE: these below are used just to
# make the above types easier to read

type Isbn = str
type Title = str
type Authors = list[str]
type Status = bool
type BorrowerId = int

type AuthorId = int
type FullName = str

type Ssn = str
type Address = str
type Phone = str

type LoanId = int
type FineId = int
type Cents = int
type IsPaid = bool

type DateOut = date
type DueDate = date
type DateIn = date

type ActiveLoanCount = int
type TotalUnpaidFines = Cents
