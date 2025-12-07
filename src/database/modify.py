
import sqlite3
from datetime import datetime

from .common import BOOK_LOANS_TABLE_NAME, BORROWERS_TABLE_NAME, FINES_TABLE_NAME
from . import config

def try_execute_many(sql: str, params: list) -> bool:
    success = True

    conn = sqlite3.connect(config.db_name)
    c = conn.cursor()

    try:
        c.executemany(sql, params)
        conn.commit()
    except sqlite3.Error as e:
        print(e)
        conn.rollback()
        success = False

    conn.close()

    return success

def try_execute_one(sql: str, params: list) -> bool:
    success = True

    conn = sqlite3.connect(config.db_name)
    c = conn.cursor()

    try:
        c.execute(sql, params)
        conn.commit()
    except sqlite3.Error as e:
        print(e)
        conn.rollback()
        success = False

    conn.close()

    return success

def create_loan(isbn: str, borrower_id: str) -> bool:
    sql = f"""
    INSERT INTO {BOOK_LOANS_TABLE_NAME} (
        Isbn,
        Card_id,
        Date_out,
        Date_in
    ) VALUES (?, ?, ?, NULL)
    """

    date_out = datetime.now().strftime('%Y-%m-%d')

    params = [isbn, borrower_id, date_out]

    return try_execute_one(sql, params)

def resolve_loan(loan_id: int) -> bool:
    sql = f"""
        UPDATE {BOOK_LOANS_TABLE_NAME}
        SET Date_in = ?
        WHERE Loan_id = ?
    """

    date_in = datetime.now().strftime('%Y-%m-%d')

    params = [date_in, loan_id]

    return try_execute_one(sql, params)

def create_borrower(name: str, ssn: str, address: str) -> bool:
    sql = f"""
    INSERT INTO {BORROWERS_TABLE_NAME} (
        Bname,
        Ssn,
        Address
    ) VALUES (?, ?, ?)
    """

    params = [name, ssn, address]

    return try_execute_one(sql, params)

def set_metadata_value(key: str, value: str) -> bool:
    sql = """
    INSERT OR REPLACE INTO metadata (
        key,
        value
    ) VALUES (
        ?,
        ?
    )
    """

    params = [key, value]

    return try_execute_one(sql, params)

def update_fines(fines: list[tuple]) -> bool:
    sql = f"""
        UPDATE {FINES_TABLE_NAME}
        SET Fine_amt = ?
        WHERE Loan_id = ?
    """

    if not fines:
        return True

    (fines, loan_ids) = tuple(map(list, zip(*fines)))

    params = [(fines, loan_ids, )]

    return try_execute_many(sql, params)

def resolve_fines(loan_ids: list[int]) -> bool:
    sql = f"""
        UPDATE {FINES_TABLE_NAME}
        SET Paid = 1
        WHERE Loan_id = ?
    """

    params = [(loan_id,) for loan_id in loan_ids]

    return try_execute_many(sql, params)
