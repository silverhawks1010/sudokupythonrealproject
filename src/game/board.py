from src.utils.constants import GRID_SIZE, BOX_SIZE


class Board:
    """Represents the 9x9 Sudoku grid and enforces placement rules."""

    def __init__(self):
        self._grid: list[list[int]] = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self._locked: list[list[bool]] = [[False] * GRID_SIZE for _ in range(GRID_SIZE)]

    def load(self, grid: list[list[int]]) -> None:
        """Load a grid from a 9x9 list of ints (0 = empty)."""
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                self._grid[r][c] = grid[r][c]
                self._locked[r][c] = grid[r][c] != 0

    def get(self, row: int, col: int) -> int:
        return self._grid[row][col]

    def is_locked(self, row: int, col: int) -> bool:
        return self._locked[row][col]

    def is_valid_placement(self, row: int, col: int, value: int) -> bool:
        """Return True if placing value at (row, col) respects Sudoku rules."""
        if value < 1 or value > GRID_SIZE:
            return False
        if self._locked[row][col]:
            return False
        for i in range(GRID_SIZE):
            if self._grid[row][i] == value:
                return False
            if self._grid[i][col] == value:
                return False
        box_r = (row // BOX_SIZE) * BOX_SIZE
        box_c = (col // BOX_SIZE) * BOX_SIZE
        for r in range(box_r, box_r + BOX_SIZE):
            for c in range(box_c, box_c + BOX_SIZE):
                if self._grid[r][c] == value:
                    return False
        return True

    def place(self, row: int, col: int, value: int) -> bool:
        """Place value on the board. Returns True on success."""
        if not self.is_valid_placement(row, col, value):
            return False
        self._grid[row][col] = value
        return True

    def clear(self, row: int, col: int) -> bool:
        """Remove a player-placed number. Returns True on success."""
        if self._locked[row][col] or self._grid[row][col] == 0:
            return False
        self._grid[row][col] = 0
        return True

    def is_complete(self) -> bool:
        """Return True if every cell is filled."""
        return all(self._grid[r][c] != 0 for r in range(GRID_SIZE) for c in range(GRID_SIZE))

    def to_list(self) -> list[list[int]]:
        return [row[:] for row in self._grid]
