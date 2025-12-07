from database.query import book
from textual import on
from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Label, Button, TabbedContent, TabPane, DataTable, Static

from ui.components import Tag

import database as db

class BookDetailModal(ModalScreen):

    def __init__(self, book_data: dict) -> None:
        super().__init__()

        self.book_data = book_data
        self.borrower_id = self.book_data['borrower_id']

        if self.borrower_id:
            borrower_data = db.get_borrower_by_id(self.borrower_id)
            self.borrower_name = borrower_data[0] if borrower_data else None

    def on_mount(self) -> None:
        table = self.query_one(DataTable)

        table.add_column("ID", width=12)
        table.add_column("Borrower ID", width=12)
        table.add_column("Date Out", width=12)
        table.add_column("Date In", width=12)

        book_loans = db.get_loans_by_isbn(self.book_data['isbn'])

        if book_loans:
            for (loan_id, _, _, borrower_id, date_out, _, date_in) in book_loans:
                table.add_row(loan_id, borrower_id, date_out, date_in)

        self.update_result_count()

    def compose(self) -> ComposeResult:
        with Container():
            with TabbedContent():
                with TabPane("Info"):
                    with Vertical():
                        yield Label("Book Details", id="modal-title")
                        yield Label(f"ISBN: {self.book_data['isbn']}", classes="detail-line")
                        yield Label(f"Title: {self.book_data['title']}", classes="detail-line")

                        with Horizontal(classes="detail-line"):
                            yield Label("Authors: ")
                            for author in self.book_data['authors']:
                                yield Tag(author.strip())

                        yield Label(f"Status: {self.book_data['status']}", classes="detail-line")
                        if self.borrower_id:
                            yield Label(
                                f"Borrower: {self.borrower_name} (ID: {self.borrower_id})",
                                classes="detail-line"
                            )

                with TabPane("Checkout History"):
                    with Vertical():
                        yield Label("Checkout History", id="modal-title")
                        yield DataTable()
                        yield Static("", id="result-count")

            yield Button("Close", id="close-button", variant="primary")

    @on(Button.Pressed)
    def handle_button_pressed(self, event: Button.Pressed) -> None:
        self.dismiss()

    @on(Tag.Clicked)
    def handle_tag_clicked(self, event: Tag.Clicked) -> None:
        self.dismiss(event.title)

    def update_result_count(self) -> None:
        table = self.query_one(DataTable)
        count = table.row_count

        item_count = self.query_one("#result-count", Static)
        item_count.update(f"{count} results found")
