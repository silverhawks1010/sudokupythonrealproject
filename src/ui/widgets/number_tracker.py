from rich.text import Text
from textual.widget import Widget

from src.game.board import Board
from src.utils.constants import GRID_SIZE

STYLE_REMAINING = "bold #c678dd"
STYLE_DONE = "strike #6b5b8c"


class NumberTracker(Widget):
    """Affiche la liste des chiffres 1-9, barrés une fois tous placés."""

    def __init__(self, board: Board, **kwargs):
        super().__init__(**kwargs)
        self.board = board

    def render(self) -> Text:
        text = Text()

        for number in range(1, GRID_SIZE + 1):
            count = sum(
                1
                for rr in range(GRID_SIZE)
                for cc in range(GRID_SIZE)
                if self.board.get(rr, cc) == number
            )
            style = STYLE_DONE if count >= GRID_SIZE else STYLE_REMAINING
            line = f" {number} \n" if number < GRID_SIZE else f" {number} "
            text.append(line, style=style)

        return text

    def refresh_tracker(self) -> None:
        self.refresh()
