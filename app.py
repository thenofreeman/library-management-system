from textual.app import App

from ui.screens import SearchScreen, HomeScreen, QuitScreen

class LibraryApp(App):
    TITLE = "Library Management System"
    SUB_TITLE = "Loading..."
    SCREENS = {
        "home": HomeScreen,
        "search": SearchScreen,
        "quit": QuitScreen,
    }

    def on_mount(self) -> None:
        # self.install_screen(SearchScreen(), name="search")
        self.push_screen('search')
        self.push_screen('quit')

app = LibraryApp()
