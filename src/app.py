from textual.app import App
from textual.binding import Binding

from ui.screens import HomeScreen

class LibraryApp(App):
    TITLE = "Library Management System"
    SUB_TITLE = ""

    CSS_PATH = [
        "ui/styles/modal.tcss"

        "ui/styles/home-screen.tcss",
        "ui/styles/book-search-screen.tcss",
        "ui/styles/borrower-search-screen.tcss",

        "ui/styles/quit-modal.tcss",
        "ui/styles/time-travel-modal.tcss",
        "ui/styles/book-detail-modal.tcss",
        "ui/styles/filter-modal.tcss",
        "ui/styles/create-borrower-modal.tcss",

        "ui/styles/navbar-component.tcss",
        "ui/styles/tag-component.tcss",
    ]

    BINDINGS = [
        Binding("q", "quit", "Quit"),
    ]

    def on_mount(self) -> None:
        self.push_screen(HomeScreen())

app = LibraryApp()
