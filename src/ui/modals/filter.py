from textual import on
from textual.app import ComposeResult
from textual.containers import Vertical, Horizontal
from textual.screen import ModalScreen
from textual.widgets import Label, Button, Select

availability_options = ['All', 'Available', 'Unavailable']

class FilterModal(ModalScreen):

    def __init__(self, filters: dict) -> None:
        super().__init__()

        self.filters = filters

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Label("Filter", classes="title")

            yield Select.from_values(
                availability_options,
                allow_blank=False,
                value=(self.filters['availability']),
                id="availability-select",
            )

            # with Horizontal(classes="date-selector"):
            #     yield Button("<", id="date-prev", classes="arrow-btn")
            #     yield Label(
            #         self.active_date.strftime("%m-%d-%Y"),
            #         id="date-display",
            #         classes="date-display",
            #     )
            #     yield Button(">", id="date-next", classes="arrow-btn")

            with Horizontal(classes="button-row"):
                yield Button("Cancel", id="cancel", variant="error")
                yield Button("Confirm", id="confirm", variant="success")

    @on(Select.Changed)
    def handle_select_changed(self, event: Select.Changed) -> None:
        if event.control.id == 'availability-select':
            self.filters['availability'] = str(event.value)

    @on(Button.Pressed)
    def handle_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "":
            pass

        elif event.button.id == "confirm":
            self.dismiss(self.filters)

        elif event.button.id == "cancel":
            self.dismiss(None)
