import sqlite3
import uuid
from datetime import datetime, date

from common import (
    BORROWER_TABLE,
    DB_NAME,
    BOOK_LOANS_TABLE,
    FINES_TABLE,
)
from logger import logger

def create_loan(isbn: str, borrower_id: str) -> bool:
    success = True

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    generated_loan_id = str(uuid.uuid4())
    date_out = datetime.now().strftime('%Y-%m-%d')

    sql = f"""
    INSERT INTO {BOOK_LOANS_TABLE} (
        Loan_id,
        Isbn,
        Card_id,
        Date_out,
        Date_in
    ) VALUES (?, ?, ?, ?, NULL)
    """

    try:
        c.execute(sql, [generated_loan_id, isbn, borrower_id, date_out])
        conn.commit()
    except sqlite3.Error as e:
        logger.error(e.__str__())

        conn.rollback()
        success = False

    conn.close()

    return success

def resolve_loan(loan_id: str) -> bool:
    success = True

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    date_in = datetime.now().strftime('%Y-%m-%d')

    sql = f"""
        UPDATE {BOOK_LOANS_TABLE}
        SET Date_in = ?
        WHERE Loan_id = ?
    """

    try:
        c.execute(sql, [date_in, loan_id])
        conn.commit()
    except sqlite3.Error as e:
        logger.error(e.__str__())

        conn.rollback()
        success = False

    conn.close()

    return success

def create_borrower(name: str, ssn: str, address: str) -> bool:
    success = True

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    sql = f"""
    INSERT INTO {BORROWER_TABLE} (
        Bname,
        Ssn,
        Address
    ) VALUES (?, ?, ?)
    """

    try:
        c.execute(sql, [name, ssn, address])
        conn.commit()
    except sqlite3.Error as e:
        logger.error(e.__str__())

        conn.rollback()
        success = False

    conn.close()

    return success

def set_metadata_value(key: str, value: str):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
    INSERT OR REPLACE INTO metadata (
        key,
        value
    ) VALUES (
        ?,
        ?
    )
    """, [key, value])
    conn.commit()

    conn.close()

def update_fines(fines: list[tuple]) -> bool:
    success = True

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    sql = f"""
        UPDATE {FINES_TABLE}
        SET Fine_amt = ?
        WHERE Loan_id = ?
    """

    (fines, loan_ids) = tuple(map(list, zip(*fines)))

    try:
        c.execute(sql, [fines, loan_ids])
        conn.commit()
    except sqlite3.Error as e:
        logger.error(e.__str__())

        conn.rollback()
        success = False

    conn.close()

    return success
