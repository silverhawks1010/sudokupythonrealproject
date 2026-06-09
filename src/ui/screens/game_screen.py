from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Label, Static

from src.game.game_session import GameSession


class GameScreen(Screen):
    """Active game screen showing the board, player info and input area."""

    def __init__(self, session: GameSession):
        super().__init__()
        self.session = session

    def compose(self) -> ComposeResult:
        yield Static(f"Player: {self.session.player.name}", id="player_info")
        yield Static(f"Score: {self.session.player.total_score}", id="score_info")
        yield Static(f"Difficulty: {self.session.difficulty}", id="difficulty_info")
        yield Label("Board will be rendered here", id="board_placeholder")
        yield Label("Press P to pause · I to interrupt", id="controls_hint")

    def on_key(self, event) -> None:
        if event.key == "p":
            self.session.pause()
        elif event.key == "i":
            self.session.interrupt()
            self.app.pop_screen()
