from rich.text import Text
from textual.reactive import reactive
from textual.widget import Widget

from src.game.board import Board
from src.utils.constants import GRID_SIZE

COL_LETTERS = "ABCDEFGHI"

STYLE_BORDER = "#4c1d95"
STYLE_HEADER = "bold #c678dd"
STYLE_LOCKED = "bold #e9d5ff"
STYLE_PLAYER = "bold #a78bfa"
STYLE_EMPTY = "#4c1d95"
STYLE_CURSOR = "bold white on #7c3aed"
STYLE_MATCH = "bold #fde047 on #3d2465"


class SudokuGrid(Widget):
    """Renders a 9x9 Sudoku board as a Textual widget."""

    cursor_row: reactive[int] = reactive(0)
    cursor_col: reactive[int] = reactive(0)

    def __init__(self, board: Board, **kwargs):
        super().__init__(**kwargs)
        self.board = board

    def render(self) -> Text:
        text = Text()

        header = "    "
        for c in range(GRID_SIZE):
            header += f" {COL_LETTERS[c]} "
            if c % 3 == 2:
                header += " "
        text.append(header + "\n", style=STYLE_HEADER)

        separator = "   +" + "---------+" * 3 + "\n"
        cursor_value = self.board.get(self.cursor_row, self.cursor_col)

        for r in range(GRID_SIZE):
            if r % 3 == 0:
                text.append(separator, style=STYLE_BORDER)

            text.append(f" {r + 1} ", style=STYLE_HEADER)
            text.append("|", style=STYLE_BORDER)
            for c in range(GRID_SIZE):
                value = self.board.get(r, c)
                cell = f" {value} " if value else " · "

                if r == self.cursor_row and c == self.cursor_col:
                    style = STYLE_CURSOR
                elif cursor_value and value == cursor_value:
                    style = STYLE_MATCH
                elif self.board.is_locked(r, c):
                    style = STYLE_LOCKED
                elif value:
                    style = STYLE_PLAYER
                else:
                    style = STYLE_EMPTY

                text.append(cell, style=style)
                if c % 3 == 2:
                    text.append("|", style=STYLE_BORDER)
            text.append("\n")

        text.append(separator, style=STYLE_BORDER)
        return text

    def move_cursor(self, dr: int, dc: int) -> None:
        self.cursor_row = max(0, min(GRID_SIZE - 1, self.cursor_row + dr))
        self.cursor_col = max(0, min(GRID_SIZE - 1, self.cursor_col + dc))

    def refresh_board(self) -> None:
        self.refresh()
