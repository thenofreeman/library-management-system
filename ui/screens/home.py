from datetime import datetime

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Button
from textual.containers import Container, Vertical, Grid

from ui.components.navbar import NavbarComponent
from ui.modals import QuitModal, TimeTravelModal
from ui.screens import SearchScreen

class HomeScreen(Screen):
    CSS = "DataTable {height: 1fr}"
    SUB_TITLE = "Home"

    # CSS_PATH = "../styles/home-screen.tcss"
    DEFAULT_CSS = """
    HomeScreen { layout: vertical; }
    HomeScreen .content { 
        height: 1fr;
        align: center middle;
    }
    HomeScreen .menu-grid {
        grid-size: 2 2;
        grid-gutter: 1 2;
        width: 70;
        height: 16;
    }
    HomeScreen .menu-btn {
        width: 100%;
        height: 100%;
    }
    """

    def __init__(self, current_date: datetime | None = None) -> None:
        super().__init__()

        self.current_date = current_date or datetime.now()

    def on_mount(self) -> None:
        pass

    def compose(self) -> ComposeResult:
        yield NavbarComponent(
            left_button=Button("Quit", id="quit-btn", variant="error"),
            right_button=Button(self.current_date.strftime("%m-%d-%Y"), id="time-travel-btn")
        )

        with Container(classes="content"):
            with Grid(classes="menu-grid"):
                yield Button("Search Books", id="search-books", classes="menu-btn", variant="primary")
                yield Button("Search Borrowers", id="search-borrowers", classes="menu-btn", variant="primary")
                yield Button("Manage Borrowers", id="manage-borrowers", classes="menu-btn", variant="primary")
                yield Button("Settings", id="settings", classes="menu-btn", variant="primary")

        # Footer (empty for now)
        yield Container(classes="footer")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "quit-btn":
            self.app.push_screen(QuitModal(), self.handle_quit)
        elif event.button.id == "time-travel-btn":
            self.app.push_screen(
                TimeTravelModal(self.current_date),
                self.handle_time_travel,
            )
        elif event.button.id == "search-books":
            self.app.push_screen(SearchScreen())
        elif event.button.id == "search-borrowers":
            self.app.push_screen(SearchScreen())
        elif event.button.id == "manage-borrowers":
            self.app.push_screen(SearchScreen())
        elif event.button.id == "settings":
            self.app.push_screen(SearchScreen())

    def handle_quit(self, should_quit: bool) -> None:
        if should_quit:
            self.app.exit()

    def handle_time_travel(self, new_date: datetime | None) -> None:
        if new_date is not None:
            self.current_date = new_date
            self.query_one("#time-travel-btn", Button).label = new_date.strftime("%m-%d-%Y")
