import os
import sqlite3
from typing import Optional

from logger import logger
from common import AUTHORS_TABLE, BOOK_AUTHORS_TABLE, BOOK_LOANS_TABLE, DB_NAME, BOOK_TABLE, BookSearchResult

def search(query: str) -> list[BookSearchResult] | None:
    """
    returns a list of "ISBN, title, authors, availability"
    """

    if not os.path.isfile(DB_NAME):
        logger.errorAll([
            f"No database found for '{DB_NAME}'",
            f"Run init command as per README"
        ])

        return

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    sql = f"""
    SELECT
        b.Isbn as Isbn,
        b.Title as Title,
        a.Name as Author,
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
    ;
    """
    params = [f"%{query}" for _ in range(3)]

    c.execute(sql, params)
    results = c.fetchall()

    conn.close()

    if not results:
        logger.error("No results from your query")

        return

    return results
