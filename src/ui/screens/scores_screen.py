from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Button, DataTable, Label

from src.data.score_manager import best_player, load_scores


class ScoresScreen(Screen):
    """Leaderboard screen with a table of all player scores."""

    def compose(self) -> ComposeResult:
        best = best_player()
        msg = f"Best player: {best[0]} ({best[1]} pts)" if best else "No scores yet."
        yield Label(msg, id="best_label")
        yield DataTable(id="scores_table")
        yield Button("Back", id="btn_back")

    def on_mount(self) -> None:
        table: DataTable = self.query_one("#scores_table", DataTable)
        table.add_columns("Player", "Score")
        for name, score in sorted(load_scores().items(), key=lambda x: -x[1]):
            table.add_row(name, str(score))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn_back":
            self.app.pop_screen()
