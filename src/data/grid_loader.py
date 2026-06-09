import os
import random

from src.game.board import Board
from src.utils.constants import GRID_SIZE, GRIDS_DIR


def load_random_grid(difficulty: str) -> Board:
    """Pick a random grid file for the given difficulty and return a loaded Board."""
    folder = os.path.join(GRIDS_DIR, difficulty)
    files = [f for f in os.listdir(folder) if f.endswith(".txt")]
    if not files:
        raise FileNotFoundError(f"No grid files found in {folder}")
    path = os.path.join(folder, random.choice(files))
    return load_grid_from_file(path)


def load_grid_from_file(path: str) -> Board:
    """Parse a grid text file and return a Board.

    File format: 9 lines of 9 space-separated integers (0 = empty).
    """
    grid: list[list[int]] = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            row = [int(x) for x in line.split()]
            if len(row) != GRID_SIZE:
                raise ValueError(f"Invalid grid row in {path}: {line!r}")
            grid.append(row)
    if len(grid) != GRID_SIZE:
        raise ValueError(f"Grid in {path} has {len(grid)} rows, expected {GRID_SIZE}")
    board = Board()
    board.load(grid)
    return board
