import sqlite3
from typing import Optional, Any

from database import config

def get_one_or_none(sql: str, params: list) -> Optional[Any]:
    conn = sqlite3.connect(config.db_name)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute(sql, params)
    result = c.fetchone()

    conn.close()

    return result

def get_all_or_none(sql: str, params: list) -> Optional[list]:
    conn = sqlite3.connect(config.db_name)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute(sql, params)
    result = c.fetchall()

    conn.close()

    return result

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
