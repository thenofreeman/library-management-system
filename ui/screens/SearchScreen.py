from textual import on
from textual.app import ComposeResult
from textual.screen import Screen
from textual.validation import Length
from textual.widgets import DataTable, Input, Label, Header

from operations import search

class SearchScreen(Screen):
    CSS = "DataTable {height: 1fr}"
    SUB_TITLE = "Search"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label("Search")
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

        table.add_columns("ISBN", "Title", "Authors", "Status")

        table.cursor_type = "row"
        table.zebra_stripes = True

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
            pass

        else:
            pass
