from textual import on
from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.validation import Length
from textual.widgets import Label, Button, TabbedContent, TabPane, DataTable, Static, Input

from models.result import BookSearchResult

from ui.components import Tag

import database as db

from ui.custom import BaseModal

class BookDetailModal(BaseModal):

    def __init__(self, book_data: BookSearchResult) -> None:
        super().__init__()

        self.book_data = book_data

        if self.book_data.borrower_id:
            self.borrower_name = db.get_borrower_by_id(self.book_data.borrower_id)

        # if self.borrower_id:
        #     borrower_data = db.get_borrower_by_id(self.borrower_id)
        #     self.borrower_name = borrower_data[0] if borrower_data else None

    def on_mount(self) -> None:
        table = self.query_one(DataTable)

        table.add_column("Loan ID", width=8)
        table.add_column("Borrower ID", width=12)
        table.add_column("Date Out", width=12)
        table.add_column("Date In", width=12)

        book_loans = db.get_loans_by_isbn(self.book_data.isbn)

        if book_loans:
            for (loan_id, _, _, borrower_id, date_out, _, date_in) in book_loans:
                table.add_row(loan_id, borrower_id, date_out, date_in)

        self.update_result_count()

    def compose(self) -> ComposeResult:
        with Container(id="modal-container"):
            yield Static("Book Details", id="modal-title")

            with Vertical(classes="form-content"):
                with TabbedContent():
                    with TabPane("Info"):
                        with Vertical():
                            yield Label(f"ISBN: {self.book_data.isbn}", classes="detail-line")
                            yield Label(f"Title: {self.book_data.title}", classes="detail-line")

                            with Horizontal(classes="detail-line"):
                                yield Label("Authors: ")
                                for author in self.book_data.authors:
                                    yield Tag(author)

                            yield Label(f"Status: {self.book_data.status_display}", classes="detail-line")
                            if self.book_data.borrower_id:
                                yield Label(
                                    f"Borrower: {self.borrower_name} (ID: {self.book_data.borrower_id})",
                                    classes="detail-line"
                                )

                    with TabPane("Manage"):
                        with Vertical():
                            if self.book_data.status == True:
                                yield Input(
                                    placeholder="Enter a Borrower ID...",
                                    type="text",
                                    validators=[
                                        Length(minimum=1)
                                    ]
                                )

                                yield Button("Check-Out Book", id="checkout-btn", variant="primary")

                            else:
                                yield Label(f"Borrower ID: {self.book_data.borrower_id}", classes="detail-line")
                                yield Label(f"Borrower Name: {self.borrower_name}", classes="detail-line")

                                loans = None
                                if self.book_data.borrower_id:
                                    loans = db.get_loans_by_borrower_id(self.book_data.borrower_id)

                                if loans:
                                    (loan_id, _, _, _, date_out, due_date, _) = loans[0]

                                    yield Label(f"Loan ID: {loan_id}", classes="detail-line")
                                    yield Label(f"Loaned On: {date_out}", classes="detail-line")
                                    yield Label(f"Due: {due_date}", classes="detail-line")

                                yield Button("Check-In Book", id="checkin-btn", variant="primary")

                    with TabPane("Checkout History"):
                        with Vertical():
                            yield DataTable()
                            yield Static("", id="result-count")

            with Horizontal(classes="form-buttons"):
                yield Button("Close", id="close-button", variant="primary")

    @on(Button.Pressed)
    def handle_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == 'close-button':
            self.dismiss()

        elif event.button.id == 'checkout-btn':
            input = self.query_one(Input)

            # TODO: shouldn't allow creating loan for the same book
            success = db.create_loan(self.book_data.isbn, input.value)

            if success:
                self.dismiss()
            else:
                pass # TODO show invalid or failed

        elif event.button.id == 'checkin-btn':
            pass # TODO: show confirm modal

    @on(Tag.Clicked)
    def handle_tag_clicked(self, event: Tag.Clicked) -> None:
        self.dismiss(event.title)

    def update_result_count(self) -> None:
        table = self.query_one(DataTable)
        count = table.row_count

        item_count = self.query_one("#result-count", Static)
        item_count.update(f"{count} results found")
