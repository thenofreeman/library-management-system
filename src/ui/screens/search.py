from textual import on
from textual.app import ComposeResult
from textual.screen import Screen
from textual.validation import Length
from textual.widgets import DataTable, Input, Button
from textual.containers import Container

from operations import search
from ui.components import NavbarComponent

class SearchScreen(Screen):
    CSS = "DataTable {height: 1fr}"
    SUB_TITLE = "Search"

    DEFAULT_CSS = """
    SearchScreen {
        layout: vertical;
    }

    SearchScreen .content {
        width: 100%;
        height: 1fr;
        align: center middle;
        padding: 2;
    }
    """

    def compose(self) -> ComposeResult:
        yield NavbarComponent(
            left_button=Button("Back", id="back-btn", variant="error"),
            right_button=Button("Filter", id="filter-btn", variant="primary"),
        )

        with Container(classes="content"):
            yield Input(
                placeholder="Search by ISBN, title, or author...",
                type="text",
                validators=[
                    Length(minimum=1)
                ]
            )

            yield DataTable()

    def on_mount(self) -> None:
        input = self.query_one(Input)

        input.focus()

        table = self.query_one(DataTable)

        table.add_column("ISBN", width=12)
        table.add_column("Title", width=50)
        table.add_column("Authors", width=25)
        table.add_column("Status", width=8)

        table.cursor_type = "row"
        table.zebra_stripes = True
    
    @on(Button.Pressed)
    def handle_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back-btn":
            self.app.pop_screen()
        # elif event.button.id == "time-travel-btn":
            # self.app.push_screen(
            #     FilterModal(),
            #     self.handle_filter,
            # )

    @on(Input.Submitted)
    def handle_search(self, event: Input.Submitted) -> None:
        table = self.query_one(DataTable)
        table.clear()

        if event.validation_result.is_valid:
            results = search(event.value)

            if not results:
                return

            for (isbn, title, authors, status) in results:
                table.add_row(isbn, title, authors, status)

        else:
            pass
