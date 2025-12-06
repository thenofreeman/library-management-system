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

    BINDINGS = [
        Binding("q", "quit", "Quit"),
    ]

    def on_mount(self) -> None:
        self.push_screen('home')

app = LibraryApp()
