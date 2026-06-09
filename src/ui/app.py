from textual.app import App, ComposeResult
from textual.binding import Binding

from src.ui.screens.menu_screen import MenuScreen


class SudokuApp(App):
    """Root Textual application."""

    TITLE = "Sudoku"
    BINDINGS = [Binding("ctrl+q", "quit", "Quit")]

    def on_mount(self) -> None:
        self.push_screen(MenuScreen())
