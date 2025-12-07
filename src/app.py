from textual.app import App
from textual.binding import Binding

from ui.screens import SearchScreen, HomeScreen

class LibraryApp(App):
    TITLE = "Library Management System"
    SUB_TITLE = ""
    SCREENS = {
        "home": HomeScreen,
        "search": SearchScreen
    }
    
    CSS_PATH = [
        "ui/styles/home-screen.tcss",
        "ui/styles/search-screen.tcss",

        "ui/styles/quit-modal.tcss",
        "ui/styles/time-travel-modal.tcss",
        "ui/styles/book-detail-modal.tcss",
        "ui/styles/filter-modal.tcss",

        "ui/styles/navbar-component.tcss",
        "ui/styles/tag-component.tcss",
    ]

    BINDINGS = [
        Binding("q", "quit", "Quit"),
    ]

    def on_mount(self) -> None:
        self.push_screen('home')

app = LibraryApp()
