from datetime import datetime, timedelta

from textual import on
from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.containers import Horizontal, Vertical
from textual.widgets import Button, Label

class TimeTravelModal(ModalScreen[datetime]):

    def __init__(self, current_date: datetime) -> None:
        super().__init__()
        self.active_date = current_date
        self.selected_date = self.active_date

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Label("Time Travel", classes="title")
            with Horizontal(classes="date-selector"):
                yield Button("<", id="date-prev", classes="arrow-btn")
                yield Label(
                    self.active_date.strftime("%m-%d-%Y"),
                    id="date-display",
                    classes="date-display",
                )
                yield Button(">", id="date-next", classes="arrow-btn")
            with Horizontal(classes="button-row"):
                yield Button("Confirm", id="confirm", variant="success")
                yield Button("Cancel", id="cancel", variant="error")

    @on(Button.Pressed)
    def handle_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "date-prev":
            if self.active_date < self.selected_date:
                self.selected_date -= timedelta(days=1)

                self.query_one("#date-display", Label).update(
                    self.selected_date.strftime("%m-%d-%Y")
                )

        elif event.button.id == "date-next":
            self.selected_date += timedelta(days=1)

            self.query_one("#date-display", Label).update(
                self.selected_date.strftime("%m-%d-%Y")
            )

        elif event.button.id == "confirm":
            self.active_date = self.selected_date

            self.dismiss(self.active_date)

        elif event.button.id == "cancel":
            self.dismiss(None)
