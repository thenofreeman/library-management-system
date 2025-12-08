
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

        self.checkouts = []
        if self.borrower_data:
            self.checkouts = db.get_loans_by_borrower_id(self.borrower_data.id, returned=False)

    def on_mount(self) -> None:
        pass

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
                                    yield SelectionList[int](
                                        *[(f"[{loan.isbn}] {loan.title}",
                                           loan.id,
                                           bool(loan.date_in)
                                           ) for loan in self.checkouts],
                                        compact=True,
                                        id="searched-columns"
                                    )

                                    yield Button("Check-in Books", id="checkin-btn", variant="primary")

                        #         if self.book_data['status'] == True:
                        #             yield Input(
                        #                 placeholder="Enter a Borrower ID...",
                        #                 type="text",
                        #                 validators=[
                        #                     Length(minimum=1)
                        #                 ]
                        #             )

                        #             yield Button("Check-Out Book", id="checkout-btn", variant="primary")

                        #         else:
                        #             yield Label(f"Borrower ID: {self.borrower_id}", classes="detail-line")
                        #             yield Label(f"Borrower Name: {self.borrower_name}", classes="detail-line")

                        #             loans = db.get_loans_by_borrower_id(self.borrower_id)

                        #             if loans:
                        #                 (loan_id, _, _, _, date_out, due_date, _) = loans[0]

                        #                 yield Label(f"Loan ID: {loan_id}", classes="detail-line")
                        #                 yield Label(f"Loaned On: {date_out}", classes="detail-line")
                        #                 yield Label(f"Due: {due_date}", classes="detail-line")

                        #             yield Button("Check-In Book", id="checkin-btn", variant="primary")

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

        elif event.button.id == 'checkin-button':
            success = db.checkin_many(self.checkouts)

            if success:
                self.dismiss()
