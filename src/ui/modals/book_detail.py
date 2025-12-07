from textual import on
from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Label, Button

from ui.components import Tag

class BookDetailModal(ModalScreen):

    def __init__(self, book_data: dict) -> None:
        super().__init__()
        self.book_data = book_data

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Label("Book Details", id="modal-title")
            yield Label(f"ISBN: {self.book_data['isbn']}", classes="detail-line")
            yield Label(f"Title: {self.book_data['title']}", classes="detail-line")

            with Horizontal(classes="detail-line"):
                yield Label("Authors: ")
                for author in self.book_data['authors']:
                    yield Tag(author.strip())

            yield Label(f"Status: {self.book_data['status']}", classes="detail-line")
            yield Button("Close", id="close-button", variant="primary")

    @on(Button.Pressed)
    def handle_button_pressed(self, event: Button.Pressed) -> None:
        self.dismiss()

    @on(Tag.Clicked)
    def handle_tag_clicked(self, event: Tag.Clicked) -> None:
        self.dismiss(event.title)
