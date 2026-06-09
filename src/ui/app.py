from pathlib import Path

from textual.app import App
from textual.binding import Binding

from src.ui.screens.menu_screen import MenuScreen


class SudokuApp(App):
    TITLE = "Sudoku — ESIEE-IT"
    SUB_TITLE = "M1 ILMSI 2025-2026"
    CSS_PATH = Path(__file__).parent / "app.tcss"
    BINDINGS = [Binding("ctrl+q", "quit", "Quitter")]

    def on_mount(self) -> None:
        self.push_screen(MenuScreen())
