from textual.app import App

from ui.screens import HomeScreen

class LibraryApp(App):
    TITLE = "Library Management System"
    SUB_TITLE = ""

    CSS_PATH = [
        "ui/styles/global/modal.tcss",
        "ui/styles/global/form.tcss",

        "ui/styles/home-screen.tcss",
        "ui/styles/search-screen.tcss",

        "ui/styles/time-travel-modal.tcss",
        "ui/styles/filter-modal.tcss",

        "ui/styles/navbar-component.tcss",
        "ui/styles/tag-component.tcss",
    ]

    def on_mount(self) -> None:
        self.push_screen(HomeScreen())

app = LibraryApp()
