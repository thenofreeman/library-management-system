from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header

class HomeScreen(Screen):
    CSS = "DataTable {height: 1fr}"
    SUB_TITLE = "Home"

    def compose(self) -> ComposeResult:
        yield Header()
        pass

    def on_mount(self) -> None:
        pass
