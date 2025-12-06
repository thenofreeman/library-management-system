from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Button, Static, Header

class NavbarComponent(Static):
    # CSS_PATH = "../styles/navbar-component.tcss"

    DEFAULT_CSS = """
    NavbarComponent {
        width: 100%;
        height: auto;
        background: $primary-background;
        layout: vertical;
    }

    NavbarComponent Header {
        dock: top;
    }

    NavbarComponent > Horizontal {
        width: 100%;
        height: 3;
    }

    NavbarComponent .nav-left {
        width: 1fr;
        height: 100%;
        align-horizontal: left;
        align-vertical: middle;
        padding: 0 1;
    }

    NavbarComponent .nav-center {
        width: 2fr;
        height: 100%;
        align-horizontal: center;
        align-vertical: middle;
    }

    NavbarComponent .nav-right {
        width: 1fr;
        height: 100%;
        align-horizontal: right;
        align-vertical: middle;
        padding: 0 1;
    }

    NavbarComponent .nav-title {
        text-style: bold;
    }

    NavbarComponent .nav-placeholder {
        width: 0;
        height: 0;
    }
    """

    def __init__(
        self,
        left_button: Button | None = None,
        title: str = "",
        right_button: Button | None = None,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)

        self.left_button = left_button
        self.title_text = title
        self.right_button = right_button

    def compose(self) -> ComposeResult:
        yield Header()

        with Horizontal():
            with Container(classes="nav-left"):
                if self.left_button:
                    yield self.left_button
                else:
                    yield Static("", classes="nav-placeholder")

            with Container(classes="nav-center"):
                yield Static(self.title_text, classes="nav-title")

            with Container(classes="nav-right"):
                if self.right_button:
                    yield self.right_button
                else:
                    yield Static("", classes="nav-placeholder")
