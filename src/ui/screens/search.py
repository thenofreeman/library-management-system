from textual import on
from textual.app import ComposeResult
from textual.screen import Screen
from textual.validation import Length
from textual.widgets import DataTable, Input, Button, Static
from textual.containers import Container

from operations import search
from ui.components import NavbarComponent
from ui.modals import BookDetailModal, FilterModal

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

    SearchScreen #result-count {
        dock: bottom;
        height: 1;
        width: 100%;
        background: $panel;
        color: $text;
        padding: 0 2;
        text-align: center;
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

            yield Static("", id="result-count")

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

        self.update_result_count()
    
    @on(Button.Pressed)
    def handle_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back-btn":
            self.app.pop_screen()
        elif event.button.id == "filter-btn":
            self.app.push_screen(
                FilterModal(),
                self.handle_filter,
            )

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

        self.update_result_count()

    def handle_filter(self, should_quit: bool) -> None:
        pass

        self.update_row_count()

    @on(DataTable.HeaderSelected)
    def handle_header_selected(self, event: DataTable.HeaderSelected) -> None:
        table = event.data_table

        table.sort(event.column_key)

    @on(DataTable.RowSelected)
    def handle_row_selected(self, event: DataTable.RowSelected) -> None:
        table = event.data_table
        row_key = event.row_key

        [isbn, title, authors, status] = table.get_row(row_key)

        book_data = {
            "id": id,
            "isbn": isbn,
            "title": title,
            "authors": authors,
            "status": status,
        }

        self.app.push_screen(BookDetailModal(book_data))

    def update_result_count(self) -> None:
        table = self.query_one(DataTable)
        count = table.row_count

        item_count = self.query_one("#result-count", Static)
        item_count.update(f"{count} results found")
