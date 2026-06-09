from enum import Enum, auto

from src.game.board import Board
from src.game.player import Player
from src.game.ia_solver import IASolver
from src.utils.constants import SCORE_WIN, SCORE_INTERRUPT


class SessionState(Enum):
    RUNNING = auto()
    PAUSED = auto()
    WON = auto()
    INTERRUPTED = auto()


class GameSession:
    """Holds the state of one ongoing Sudoku game."""

    def __init__(self, player: Player, difficulty: str, board: Board):
        self.player = player
        self.difficulty = difficulty
        self.board = board
        self.state = SessionState.RUNNING
        self.session_score: int = 0
        self._ia = IASolver(board)

    def human_place(self, row: int, col: int, value: int) -> bool:
        """Place a number for the human player. Returns True on success."""
        if self.state != SessionState.RUNNING:
            return False
        ok = self.board.place(row, col, value)
        if ok and self.board.is_complete():
            self._finish_win()
        return ok

    def human_clear(self, row: int, col: int) -> bool:
        """Remove a player-placed number."""
        if self.state != SessionState.RUNNING:
            return False
        return self.board.clear(row, col)

    def ia_step(self) -> tuple[int, int, int] | None:
        """Make one IA move. Returns (row, col, value) or None when done."""
        if self.state != SessionState.RUNNING:
            return None
        move = self._ia.next_move()
        if move:
            row, col, value = move
            self.board.place(row, col, value)
            if self.board.is_complete():
                self._finish_win()
        return move

    def pause(self) -> None:
        if self.state == SessionState.RUNNING:
            self.state = SessionState.PAUSED

    def resume(self) -> None:
        if self.state == SessionState.PAUSED:
            self.state = SessionState.RUNNING

    def interrupt(self) -> None:
        if self.state == SessionState.RUNNING:
            self.state = SessionState.INTERRUPTED
            self.session_score = SCORE_INTERRUPT[self.difficulty]
            self.player.apply_score(self.session_score)

    def _finish_win(self) -> None:
        self.state = SessionState.WON
        self.session_score = SCORE_WIN[self.difficulty]
        self.player.apply_score(self.session_score)
