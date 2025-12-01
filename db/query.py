import sqlite3
from datetime import date

from common import (
    BORROWER_TABLE,
    DB_NAME,
    BOOK_TABLE,
    BOOK_AUTHORS_TABLE,
    AUTHORS_TABLE,
    BOOK_LOANS_TABLE,
    FINES_TABLE,
    BorrowerSearchResult
)
from logger import logger

def get_checkouts(borrower_id: str | None = None) -> list:
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    if borrower_id:
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
    else:
        sql = f"""
        SELECT
            b.Isbn,
            b.Title,
            l.Date_out,
            l.Date_in,
            l.Loan_id,
        FROM {BOOK_TABLE} b
        JOIN {BOOK_LOANS_TABLE} l ON l.Isbn = b.Isbn
        AND l.Date_in IS NULL
        """

        c.execute(sql, [borrower_id])

    return c.fetchall()

def book_exists(isbn: str) -> bool:
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    sql = f"""
    SELECT
        Isbn
    FROM {BOOK_TABLE}
    WHERE Isbn = ?
    """

    c.execute(sql, [isbn])
    result = c.fetchone()

    if result:
        return result[0] # as boolean

    return False

def is_available(isbn: str) -> bool:
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

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

    return is_checked_out == 1

def get_fines(borrower_id: str) -> list:
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

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

    return c.fetchall()

def search_checkouts(isbn: str, borrower_id: str, name: str) -> list[BorrowerSearchResult] | None:
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    sql = """
    SELECT
        l.Loan_id,
        l.Isbn,
        b.Title,
        l.Card_id,
        br.Bname
    FROM BOOK_LOANS l
    JOIN BOOK b ON b.Isbn = l.Isbn
    JOIN BORROWER br ON br.Card_id = l.Card_id
    WHERE l.Date_in IS NULL
    """

    conditions = []
    params = []

    if isbn:
        conditions.append("l.Isbn LIKE ? COLLATE NOCASE")
        params.append(f"%{isbn}%")

    if borrower_id:
        conditions.append("br.Card_id LIKE ?")
        params.append(f"%{isbn}%")

    if name:
        conditions.append("br.Bname LIKE ? COLLATE NOCASE")
        params.append(f"%{isbn}%")

    if conditions:
        sql += " AND (" + " OR ".join(conditions) + ")"

    sql += " ORDER BY l.Date_out DESC"

    c.execute(sql, params)
    checkouts = c.fetchall()

    conn.close()

    if not checkouts:
        logger.error(f"No matching results.")

    return checkouts

def search_books(query: str) -> list:
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    sql = f"""
    SELECT
        b.Isbn as Isbn,
        b.Title as Title,
        GROUP_CONCAT(a.Name, ', ') as Authors,
        CASE
            WHEN l.Isbn IS NULL THEN 1
            WHEN l.Date_in IS NOT NULL THEN 1
            ELSE 0
        END as Status
    FROM {BOOK_TABLE} b
    LEFT JOIN {BOOK_AUTHORS_TABLE} ba ON ba.Isbn = b.Isbn
    LEFT JOIN {AUTHORS_TABLE} a ON a.Author_id = ba.Author_id
    LEFT JOIN {BOOK_LOANS_TABLE} l ON b.Isbn = l.Isbn AND l.Date_in IS NULL
    WHERE b.Isbn LIKE ? COLLATE NOCASE
       OR b.Title LIKE ? COLLATE NOCASE
       OR a.Name LIKE ? COLLATE NOCASE
    GROUP BY b.Isbn, b.Title, l.Isbn, l.Date_in
    """
    params = [f"%{query}%" for _ in range(3)]

    c.execute(sql, params)
    results = c.fetchall()

    conn.close()

    return results

def get_borrower_id(ssn: str) -> int | None:
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    sql = f"""
    SELECT
        Card_id
    FROM {BORROWER_TABLE}
    WHERE Ssn = ?
    """

    c.execute(sql, [ssn])
    result = c.fetchone()

    conn.close()

    if result:
        return result[0]

    return result

def borrower_exists(ssn: str) -> bool:
    return get_borrower_id(ssn) is not None # as boolean

def last_updated_fines() -> date | None:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT value FROM metadata
        WHERE key = ?
    """, (
        'last_update',
    ))
    row = cursor.fetchone()
    last_update = date.fromisoformat(row[0]) if row else None

    conn.close()

    return last_update
