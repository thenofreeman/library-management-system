from typing import Optional

from textual.widgets import Input

from ui.screens import SearchScreen
from ui.modals import BookDetailModal

from database.dtypes import Book

import database as db

class BookSearchScreen(SearchScreen):

    def __init__(self):
        def book_search(query: str, filters: Optional[dict]) -> Optional[list[Book]]:
            return db.search_books(query)

        super().__init__(
            title="Book Search",
            columns=[
                ("ISBN", 12),
                ("Title", 50),
                ("Authors", 25),
                ("Status", 8),
                ("Borrower ID", 12),
            ],
            search_fn=book_search,
            detail_modal=BookDetailModal,
            placeholder="Search by ISBN, title, or author...",
            on_detail_callback=self.handle_author_selected,
            filters={
                'columns': [('ISBN', True), ('Title', True), ('Authors', True)],
                'availability': 'All',
            }
        )

    def get_detail_data(self, row_data: tuple) -> dict:
        isbn, title, authors, status, borrower_id = row_data

        return {
            "id": isbn,
            "isbn": isbn,
            "title": title,
            "authors": authors.strip().split(','),
            "status": status,
            "borrower_id": borrower_id,
        }

    def handle_author_selected(self, author_name: str | None) -> None:
        if author_name:
            input = self.query_one(Input)
            input.value = author_name
            self.handle_search(input.value)
