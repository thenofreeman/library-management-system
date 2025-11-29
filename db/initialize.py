import sqlite3

from common import (
    DB_NAME,
    BOOK_TABLE,
    BOOK_AUTHORS_TABLE,
    BOOK_LOANS_TABLE,
    AUTHORS_TABLE,
    BORROWER_TABLE,
    FINES_TABLE,
)
from logger import logger

def create_database() -> None:
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
            Card_id INTEGER AUTO INCREMENT,
            Ssn TEXT NOT NULL,
            Bname TEXT NOT NULL,
            Address TEXT NOT NULL,
            Phone TEXT,

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

    logger.write(f"Creating DB file '{DB_NAME}'...")

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    logger.write("Creating tables...\n")

    c.execute(create_books_table)
    c.execute(create_book_authors_table)
    c.execute(create_authors_table)
    c.execute(create_borrower_table)
    c.execute(create_book_loans_table)
    c.execute(create_fines_table)

    conn.close()

    # conn = sqlite3.connect(DB_NAME)
    # c = conn.cursor()

    # c.execute(f"""
    #     SELECT MAX(Card_id) FROM {BORROWER_TABLE};
    # """)
    # max_id = c.fetchone()[0]
    # print(max_id)

    # c.execute(f"""
    #     UPDATE sqlite_sequence
    #     SET seq = ?
    #     WHERE name = ?;
    # """, [max_id, BORROWER_TABLE])

    logger.write("Tables created.")
    logger.write()

    conn.close()

    logger.write(f"Database successfully created at {DB_NAME}.")


def init_books(data: list[list[str]]) -> None:
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    sql = f"""INSERT INTO {BOOK_TABLE} (
        Isbn, Title
    ) VALUES (
        ?, ?
    );"""

    book_data = [tuple(row) for row in data[1:]]

    try:
        c.executemany(sql, book_data)
        conn.commit()
    except sqlite3.Error as e:
        logger.error(e.__str__())

        conn.rollback()

    conn.close()

def init_book_authors(data: list[list[str]]) -> None:
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # TODO: shouldn't ignore... there is an issue with the normalize code
    sql = f"""INSERT OR IGNORE INTO {BOOK_AUTHORS_TABLE} (
        Author_id, Isbn
    ) VALUES (
        ?, ?
    );"""

    book_authors_data = [tuple(row) for row in data[1:]]

    try:
        c.executemany(sql, book_authors_data)
        conn.commit()
    except sqlite3.Error as e:
        logger.error(e.__str__())

        conn.rollback()

    conn.close()

def init_authors(data: list[list[str]]) -> None:
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    sql = f"""INSERT INTO {AUTHORS_TABLE} (
        Author_id, Name
    ) VALUES (
        ?, ?
    );"""

    authors_data = [tuple(row) for row in data[1:]]

    try:
        c.executemany(sql, authors_data)
        conn.commit()
    except sqlite3.Error as e:
        logger.error(e.__str__())

        conn.rollback()

    conn.close()

def init_borrowers(data: list[list[str]]) -> None:
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    sql = f"""INSERT INTO {BORROWER_TABLE} (
        Card_id, Ssn, Bname, Address, Phone
    ) VALUES (
        ?, ?, ?, ?, ?
    );"""

    borrowers_data = [tuple(row) for row in data[1:]]

    try:
        c.executemany(sql, borrowers_data)
        conn.commit()
    except sqlite3.Error as e:
        logger.error(e.__str__())

        conn.rollback()

    conn.close()
