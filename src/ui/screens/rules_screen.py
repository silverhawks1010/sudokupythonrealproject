from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Button, Markdown


RULES_TEXT = """\
# Sudoku Rules

Fill every row, column and 3×3 box with the digits **1–9** without repeating any digit
in the same row, column or box.

## Controls
- Enter a row number (1–9) and a column letter (A–I), then the value.
- Press **C** before a move to clear that cell instead.
- Press **P** to pause and save.
- Press **I** to interrupt (no save, negative score).
"""


class RulesScreen(Screen):
    """Displays the game rules."""

    def compose(self) -> ComposeResult:
        yield Markdown(RULES_TEXT)
        yield Button("Back", id="btn_back")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn_back":
            self.app.pop_screen()
