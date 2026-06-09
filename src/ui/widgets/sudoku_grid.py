from textual.widget import Widget
from textual.reactive import reactive

from src.game.board import Board
from src.utils.constants import GRID_SIZE


class SudokuGrid(Widget):
    """Renders a 9x9 Sudoku board as a Textual widget."""

    cursor_row: reactive[int] = reactive(0)
    cursor_col: reactive[int] = reactive(0)

    def __init__(self, board: Board, **kwargs):
        super().__init__(**kwargs)
        self.board = board

    def render(self) -> str:
        col_headers = "    " + "  ".join("ABCDEFGHI")
        lines = [col_headers, "   +" + "-------+" * 3]
        for r in range(GRID_SIZE):
            if r in (3, 6):
                lines.append("   +" + "-------+" * 3)
            row_parts = []
            for c in range(GRID_SIZE):
                val = self.board.get(r, c)
                cell = str(val) if val != 0 else "."
                if r == self.cursor_row and c == self.cursor_col:
                    cell = f"[{cell}]"
                row_parts.append(cell)
            row_str = " ".join(
                " ".join(row_parts[i * 3:(i + 1) * 3]) for i in range(3)
            )
            lines.append(f" {r + 1} | {row_str} |")
        lines.append("   +" + "-------+" * 3)
        return "\n".join(lines)

    def move_cursor(self, dr: int, dc: int) -> None:
        self.cursor_row = max(0, min(GRID_SIZE - 1, self.cursor_row + dr))
        self.cursor_col = max(0, min(GRID_SIZE - 1, self.cursor_col + dc))
