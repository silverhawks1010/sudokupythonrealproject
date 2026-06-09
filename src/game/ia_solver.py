from src.game.board import Board
from src.utils.constants import GRID_SIZE


class IASolver:
    """Automatic player that fills the board using backtracking."""

    def __init__(self, board: Board):
        self._board = board

    def next_move(self) -> tuple[int, int, int] | None:
        """Return (row, col, value) for the next valid move, or None if none found."""
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if self._board.get(row, col) == 0:
                    for value in range(1, GRID_SIZE + 1):
                        if self._board.is_valid_placement(row, col, value):
                            return (row, col, value)
        return None

    def solve_all(self) -> bool:
        """Fill the entire board using backtracking. Returns True if solved."""
        empty = self._find_empty()
        if empty is None:
            return True
        row, col = empty
        for value in range(1, GRID_SIZE + 1):
            if self._board.place(row, col, value):
                if self.solve_all():
                    return True
                self._board.clear(row, col)
        return False

    def _find_empty(self) -> tuple[int, int] | None:
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if self._board.get(row, col) == 0:
                    return (row, col)
        return None
