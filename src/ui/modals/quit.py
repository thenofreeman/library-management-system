from textual import on
from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.containers import Grid
from textual.widgets import Button, Label

class QuitModal(ModalScreen[bool]):

    def compose(self) -> ComposeResult:
        yield Grid(
            Label("Are you sure you want to quit?", id="question"),
            Button("Quit", variant="error", id="quit-btn"),
            Button("Cancel", variant="primary", id="cancel-btn"),
            id="dialog",
        )

    @on(Button.Pressed)
    def handle_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "quit-btn":
            self.app.exit()
            self.dismiss(True)
        else:
            self.app.pop_screen()
            self.dismiss(False)
