from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Button, DataTable, Footer, Label, Rule

from src.data.score_manager import best_player, load_scores
from src.ui.widgets.score_chart import show_scores_chart


class ScoresScreen(Screen):
    """Classement de tous les joueurs."""

    BINDINGS = [Binding("escape", "go_back", "Retour")]

    def compose(self) -> ComposeResult:
        best = best_player()
        best_msg = (
            f"Meilleur joueur : {best[0]}  ({best[1]} pts)" if best
            else "Aucun score enregistré."
        )
        with Vertical(id="scores_card"):
            yield Label("Scores", id="scores_title")
            yield Label(best_msg, id="best_label")
            yield Rule()
            yield DataTable(id="scores_table")
            with Horizontal(id="scores_btn_row"):
                yield Button("Graphique", id="btn_chart", variant="default")
                yield Button("Retour", id="btn_back_scores", variant="default")
        yield Footer()

    def on_mount(self) -> None:
        table: DataTable = self.query_one("#scores_table", DataTable)
        table.add_columns("Joueur", "Score")
        for name, score in sorted(load_scores().items(), key=lambda x: -x[1]):
            table.add_row(name, str(score))
        if table.row_count == 0:
            table.add_row("—", "—")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn_back_scores":
            self.action_go_back()
        elif event.button.id == "btn_chart":
            if not load_scores():
                self.app.notify("Aucun score à afficher.", severity="warning")
                return
            with self.app.suspend():
                show_scores_chart()

    def action_go_back(self) -> None:
        self.app.pop_screen()
