from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Center, Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Static

from src.data.save_manager import write_save, delete_save
from src.data.score_manager import save_score
from src.game.game_session import GameSession, SessionState
from src.ui.widgets.number_tracker import NumberTracker
from src.ui.widgets.sudoku_grid import COL_LETTERS, SudokuGrid
from src.utils.constants import (
    DIFFICULTY_DIFFICULT,
    DIFFICULTY_EASY,
    DIFFICULTY_INTERMEDIATE,
)

DIFFICULTY_LABELS = {
    DIFFICULTY_EASY: "Facile",
    DIFFICULTY_INTERMEDIATE: "Intermédiaire",
    DIFFICULTY_DIFFICULT: "Difficile",
}


class GameScreen(Screen):
    """Écran de jeu : grille, infos joueur et saisie au clavier."""

    BINDINGS = [
        Binding("up", "move(-1,0)", "Haut", show=False),
        Binding("down", "move(1,0)", "Bas", show=False),
        Binding("left", "move(0,-1)", "Gauche", show=False),
        Binding("right", "move(0,1)", "Droite", show=False),
        Binding("1", "place(1)", "1", show=False),
        Binding("2", "place(2)", "2", show=False),
        Binding("3", "place(3)", "3", show=False),
        Binding("4", "place(4)", "4", show=False),
        Binding("5", "place(5)", "5", show=False),
        Binding("6", "place(6)", "6", show=False),
        Binding("7", "place(7)", "7", show=False),
        Binding("8", "place(8)", "8", show=False),
        Binding("9", "place(9)", "9", show=False),
        Binding("0", "clear_cell", "Effacer", show=False),
        Binding("delete", "clear_cell", "Effacer", show=False),
        Binding("backspace", "clear_cell", "Effacer", show=False),
        Binding("n", "ia_step", "Coup IA"),
        Binding("p", "pause", "Pause"),
        Binding("i", "interrupt", "Interrompre"),
    ]

    def __init__(self, session: GameSession):
        super().__init__()
        self.session = session

    def compose(self) -> ComposeResult:
        if self.session.is_ia:
            footer_text = "N : coup de l'IA · P : pause · I : interrompre"
        else:
            footer_text = (
                "Flèches : déplacer · 1-9 : placer · 0 : effacer · "
                "P : pause · I : interrompre"
            )
        yield Static(footer_text, id="game_footer")

        with Center():
            with Vertical(id="game_card"):
                with Horizontal(id="game_header"):
                    yield Static(
                        f"Joueur : {self.session.player.name}", id="player_info"
                    )
                    yield Static(
                        f"Score : {self.session.player.total_score}", id="score_info"
                    )
                    yield Static(
                        f"Niveau : {DIFFICULTY_LABELS[self.session.difficulty]}",
                        id="difficulty_info",
                    )

                with Horizontal(id="game_body"):
                    yield NumberTracker(self.session.board, id="number_tracker")
                    with Center(id="grid_wrapper"):
                        yield SudokuGrid(self.session.board, id="sudoku_grid")
                yield Static("", id="message_info")

    def action_move(self, dr: int, dc: int) -> None:
        if self.session.is_ia:
            return
        self.query_one(SudokuGrid).move_cursor(dr, dc)

    def action_place(self, value: int) -> None:
        if self.session.is_ia or self.session.state != SessionState.RUNNING:
            return

        grid = self.query_one(SudokuGrid)
        row, col = grid.cursor_row, grid.cursor_col

        if self.session.board.is_locked(row, col):
            self._set_message("Cette case est verrouillée.", error=True)
            return

        if self.session.human_place(row, col, value):
            grid.refresh_board()
            self.query_one(NumberTracker).refresh_tracker()
            self._set_message(f"{value} placé en {COL_LETTERS[col]}{row + 1}.")
            self._refresh_score()
            if self.session.state == SessionState.WON:
                self._on_win()
        else:
            self._set_message("Placement invalide !", error=True)

    def action_clear_cell(self) -> None:
        if self.session.is_ia or self.session.state != SessionState.RUNNING:
            return

        grid = self.query_one(SudokuGrid)
        row, col = grid.cursor_row, grid.cursor_col

        if self.session.human_clear(row, col):
            grid.refresh_board()
            self.query_one(NumberTracker).refresh_tracker()
            self._set_message(f"Case {COL_LETTERS[col]}{row + 1} effacée.")
        else:
            self._set_message("Rien à effacer ici.", error=True)

    def action_ia_step(self) -> None:
        if not self.session.is_ia or self.session.state != SessionState.RUNNING:
            return

        move = self.session.ia_step()
        if move is None:
            self._set_message("L'IA est bloquée, aucun coup possible.", error=True)
            return

        row, col, value = move
        self.query_one(SudokuGrid).refresh_board()
        self.query_one(NumberTracker).refresh_tracker()
        self._set_message(f"IA : {value} placé en {COL_LETTERS[col]}{row + 1}.")
        self._refresh_score()
        if self.session.state == SessionState.WON:
            self._on_win()

    def action_pause(self) -> None:
        if self.session.state != SessionState.RUNNING:
            return

        self.session.pause()
        write_save(
            {
                "player_name": self.session.player.name,
                "difficulty": self.session.difficulty,
                "board": self.session.board.to_list(),
                "total_score": self.session.player.total_score,
            }
        )
        self.app.notify("Partie mise en pause et sauvegardée.", title="Pause")
        self.app.pop_screen()

    def action_interrupt(self) -> None:
        if self.session.state != SessionState.RUNNING:
            return

        self.session.interrupt()
        delete_save()
        save_score(self.session.player.name, self.session.player.total_score)
        self.app.notify(
            f"Partie interrompue. Score : {self.session.session_score:+d}",
            title="Abandon",
            severity="warning",
        )
        self.app.pop_screen()

    def _on_win(self) -> None:
        delete_save()
        save_score(self.session.player.name, self.session.player.total_score)
        self.app.notify(
            f"Bravo {self.session.player.name} ! Grille terminée. "
            f"Score : {self.session.session_score:+d} "
            f"(total : {self.session.player.total_score})",
            title="Victoire !",
        )
        self.app.pop_screen()

    def _refresh_score(self) -> None:
        self.query_one("#score_info", Static).update(
            f"Score : {self.session.player.total_score}"
        )

    def _set_message(self, message: str, error: bool = False) -> None:
        color = "#fca5a5" if error else "#a78bfa"
        self.query_one("#message_info", Static).update(f"[{color}]{message}[/{color}]")
