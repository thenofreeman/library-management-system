from textual.app import ComposeResult
from textual.containers import Container
from textual.screen import ModalScreen
from textual.widgets import Label, Button

class FilterModal(ModalScreen):

    def __init__(self) -> None:
        super().__init__()

    def compose(self) -> ComposeResult:
        with Container(id="modal-container"):
            yield Label(f"Test: blah", classes="detail-line")
            yield Button("Close", id="close-button", variant="primary")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.dismiss()
