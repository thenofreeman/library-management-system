from typing import Callable, Any, Optional

from textual import on
from textual.app import ComposeResult
from textual.screen import Screen
from textual.validation import Length
from textual.widgets import DataTable, Input, Button, Static
from textual.containers import Container

from ui.components import NavbarComponent
from ui.modals import FilterModal

class SearchScreen(Screen):

    def __init__(
        self,
        title: str,
        columns: list[tuple[str, int]],
        search_fn: Callable[[str, Optional[dict]], list],
        detail_modal: type,
        filters: Optional[dict] = None,
        placeholder: str = "Search...",
        on_detail_callback: Optional[Callable[[Any], None]] = None,
    ):
        super().__init__()

        self.SUB_TITLE = title
        self.columns = columns
        self.search_fn = search_fn
        self.detail_modal = detail_modal
        self.placeholder = placeholder
        self.on_detail_callback = on_detail_callback
        self.filters = filters

        self.results = []

    def compose(self) -> ComposeResult:
        right_button = (
            Button("Filter", id="filter-btn", variant="primary") if self.filters else None
        )

        yield NavbarComponent(
            left_button=Button("Back", id="back-btn", variant="error"),
            right_button=right_button,
        )

        with Container(classes="content"):
            yield Input(
                placeholder=self.placeholder,
                type="text",
                validators=[Length(minimum=1)]
            )
            yield DataTable()
            yield Static("", id="result-count")

    def on_mount(self) -> None:
        input = self.query_one(Input)
        input.focus()

        table = self.query_one(DataTable)

        for col_name, width in self.columns:
            table.add_column(col_name, width=width)

        table.cursor_type = "row"
        table.zebra_stripes = True

        self.update_result_count()

    @on(Button.Pressed)
    def handle_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back-btn":
            self.app.pop_screen()

        elif event.button.id == "filter-btn" and self.filters:
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

        self.results = self.search_fn(value, self.filters)

        if not self.results:
            self.update_result_count()
            return

        for row_data in self.results:
            table.add_row(*row_data.model_dump().values(), key=str(row_data.id))

        self.update_result_count()

    def handle_filter(self, filters: dict) -> None:
        if not filters:
            return None

        self.filters = filters

        input = self.query_one(Input)
        if input.value:
            self.handle_search(input.value)
        else:
            self.update_result_count()

    @on(DataTable.HeaderSelected)
    def handle_header_selected(self, event: DataTable.HeaderSelected) -> None:
        table = event.data_table
        table.sort(event.column_key)

    @on(DataTable.RowSelected)
    def handle_row_selected(self, event: DataTable.RowSelected) -> None:
        row_data = next(m for m in self.results if str(m.id) == event.row_key)

        data = self.get_detail_data(row_data)

        self.app.push_screen(
            self.detail_modal(data),
            self.handle_detail_response
        )

    def handle_detail_response(self, response: Any) -> None:
        if self.on_detail_callback:
            self.on_detail_callback(response)

    def update_result_count(self) -> None:
        table = self.query_one(DataTable)
        count = table.row_count

        item_count = self.query_one("#result-count", Static)
        item_count.update(f"{count} results found")
