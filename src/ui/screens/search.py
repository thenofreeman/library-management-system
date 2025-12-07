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
    SUB_TITLE = "Search"

    def __init__(self):
        super().__init__()

        self.filters = {
            'columns': [('ISBN', True), ('Title', True), ('Authors', True)],
            'availability': 'All',
        }

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
                FilterModal(self.filters),
                self.handle_filter,
            )

    @on(Input.Submitted)
    def handle_submit(self, event: Input.Submitted) -> None:
        if event.validation_result.is_valid:
            self.handle_search(event.value)

    def handle_search(self, value: str) -> None:
        table = self.query_one(DataTable)
        table.clear()

        results = search(value)

        if not results:
            return

        for (isbn, title, authors, status) in results:
            table.add_row(isbn, title, authors, status)

        self.update_result_count()

    def handle_filter(self, filters: dict) -> None:
        if not filters:
            return None

        self.filters = filters

        self.update_result_count()

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
            "authors": authors.strip().split(','),
            "status": status,
        }

        self.app.push_screen(BookDetailModal(book_data), self.handle_author_selected)

    def handle_author_selected(self, author_name: str | None) -> None:
        if author_name:
            input = self.query_one(Input)
            input.value = author_name

            self.handle_search(input.value)

    def update_result_count(self) -> None:
        table = self.query_one(DataTable)
        count = table.row_count

        item_count = self.query_one("#result-count", Static)
        item_count.update(f"{count} results found")
