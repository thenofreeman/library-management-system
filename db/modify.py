import sqlite3
import uuid
from datetime import datetime

from common import (
    DB_NAME,
    BOOK_LOANS_TABLE,
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
