from textual.app import ComposeResult
from textual.containers import Container
from textual.screen import ModalScreen
from textual.widgets import Label, Button

class BookDetailModal(ModalScreen):

    def __init__(self, book_data: dict) -> None:
        super().__init__()
        self.book_data = book_data

    def compose(self) -> ComposeResult:
        with Container(id="modal-container"):
            yield Label("Book Details", id="modal-title")
            yield Label(f"ISBN: {self.book_data['isbn']}", classes="detail-line")
            yield Label(f"Title: {self.book_data['title']}", classes="detail-line")
            yield Label(f"Authors: {self.book_data['authors']}", classes="detail-line")
            yield Label(f"Status: {self.book_data['status']}", classes="detail-line")
            yield Button("Close", id="close-button", variant="primary")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.dismiss()
