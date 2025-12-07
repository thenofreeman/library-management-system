from textual import on
from textual.app import ComposeResult
from textual.containers import Container, Vertical, Horizontal
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label, Static
from textual.binding import Binding

class CreateBorrowerModal(ModalScreen):
    BINDINGS = [
        Binding("escape", "dismiss", "Cancel"),
    ]

    def compose(self) -> ComposeResult:
        with Container(id="modal_container"):
            yield Static("Enter Borrower Information", id="title")

            with Vertical(classes="input_group"):
                yield Label("Name:", classes="input_label")
                yield Input(placeholder="Enter full name", id="name_input")

            with Vertical(classes="input_group"):
                yield Label("SSN:", classes="input_label")
                yield Input(placeholder="XXX-XX-XXXX", id="ssn_input")

            with Vertical(classes="input_group"):
                yield Label("Address:", classes="input_label")
                yield Input(placeholder="Enter address", id="address_input")

            with Vertical(classes="input_group"):
                yield Label("Phone:", classes="input_label")
                yield Input(placeholder="(XXX) XXX-XXXX", id="phone_input")

            with Horizontal(id="button_container"):
                yield Button("Submit", variant="primary", id="submit_btn")
                yield Button("Cancel", variant="default", id="cancel_btn")

    @on(Button.Pressed)
    def handle_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "submit_btn":
            name = self.query_one("#name_input", Input).value
            ssn = self.query_one("#ssn_input", Input).value
            address = self.query_one("#address_input", Input).value
            phone = self.query_one("#phone_input", Input).value

            data = {
                "name": name,
                "ssn": ssn,
                "address": address,
                "phone": phone
            }

            success = False # TODO: do something with the data

            if success:
                self.dismiss(data)

        elif event.button.id == "cancel_btn":
            self.dismiss(None)
