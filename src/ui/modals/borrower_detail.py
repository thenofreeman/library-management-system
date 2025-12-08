
from models.result import BorrowerSearchResult
from textual import on
from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Label, Button, TabbedContent, TabPane, DataTable, Static, Input, SelectionList

from ui.custom import BaseModal

import database as db

class BorrowerDetailModal(BaseModal):

    def __init__(self, borrower_result: BorrowerSearchResult) -> None:
        super().__init__()

        self.borrower_data = db.get_borrower_by_id(borrower_result.id)

        self.active_checkouts = []
        self.all_checkouts = []

        if self.borrower_data:
            self.active_checkouts = db.get_loans_by_borrower_id(self.borrower_data.id, returned=False)
            self.all_checkouts = db.get_loans_by_borrower_id(self.borrower_data.id, returned=True)

    def on_mount(self) -> None:
        table = self.query_one(DataTable)

        table.zebra_stripes = True

        table.add_columns(*["Loan", "ISBN", "Date Out", "In"])
        for loan in self.all_checkouts:
            table.add_row(loan.id, loan.isbn, loan.date_out, loan.date_in)

    def compose(self) -> ComposeResult:
        with Container(id="modal-container"):
            yield Static("Borrower Details", id="modal-title")

            with Vertical(classes="form-content"):
                if not self.borrower_data:
                    yield Label(f"Unable to access borrower data")
                else:
                    with TabbedContent():
                        with TabPane("Info"):
                            with Vertical():
                                yield Label(f"Card ID: {self.borrower_data.id}", classes="detail-line")
                                yield Label(f"Full Name: {self.borrower_data.name}", classes="detail-line")
                                yield Label(f"SSN: {self.borrower_data.ssn}", classes="detail-line")
                                yield Label(f"Address: {self.borrower_data.address}", classes="detail-line")
                                yield Label(f"Phone: {self.borrower_data.phone}", classes="detail-line")

                        with TabPane("Manage"):
                            with Vertical():
                                with Vertical(classes="input-field"):
                                    yield Label("Active Checkouts")

                                    if not self.active_checkouts:
                                        yield Label("No Checkouts")
                                    else:
                                        yield SelectionList[int](
                                            *[(f"[{loan.isbn}] {loan.title}",
                                            loan.id,
                                            bool(loan.date_in)
                                            ) for loan in self.active_checkouts],
                                            compact=True,
                                            id="searched-columns"
                                        )

                                        yield Button("Check-in Books", id="checkin-button", variant="primary")

                        with TabPane("Checkout History"):
                            with Vertical():
                                yield DataTable(

                                )
                                yield Static("", id="result-count")

                with Horizontal(classes="form-buttons"):
                    yield Button("Close", id="close-button", variant="primary")

    @on(Button.Pressed)
    def handle_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == 'close-button':
            self.dismiss()

        elif event.button.id == 'checkin-button':
            selection_list = self.query_one(SelectionList)

            selected_items = [
                self.active_checkouts[idx-1]
                for idx in selection_list.selected
            ]

            if selected_items:
                success = db.checkin_many(selected_items)

                if success:
                    self.dismiss()
