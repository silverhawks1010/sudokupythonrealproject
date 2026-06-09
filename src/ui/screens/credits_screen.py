from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Button, Markdown


CREDITS_TEXT = """\
# Credits

**Sudoku — ESIEE-IT M1 ILMSI 2025-2026**

Developed as part of the Python programming project.

*Elisabeth Rendler* — project supervisor
"""


class CreditsScreen(Screen):
    """Displays team credits."""

    def compose(self) -> ComposeResult:
        yield Markdown(CREDITS_TEXT)
        yield Button("Back", id="btn_back")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn_back":
            self.app.pop_screen()
