from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Button, Footer, Input, Label, RadioButton, RadioSet, Rule

from src.utils.constants import DIFFICULTY_EASY, DIFFICULTY_INTERMEDIATE, DIFFICULTY_DIFFICULT


class NewGameScreen(Screen):
    """Formulaire de lancement d'une nouvelle partie."""

    BINDINGS = [Binding("escape", "go_back", "Retour")]

    def compose(self) -> ComposeResult:
        with Vertical(id="new_game_card"):
            yield Label("Nouvelle Partie", id="new_game_title")
            yield Rule()

            yield Label("Nom du joueur :", classes="field-label")
            yield Input(placeholder="Entrez votre nom…", id="player_input")

            yield Label("Niveau de difficulté :", classes="field-label")
            with RadioSet(id="difficulty_set"):
                yield RadioButton("Facile",         id="radio_easy",         value=True)
                yield RadioButton("Intermédiaire",  id="radio_intermediate")
                yield RadioButton("Difficile",      id="radio_difficult")

            with Horizontal(id="btn_row"):
                yield Button("Commencer", id="btn_start",   variant="success")
                yield Button("Retour",    id="btn_back_ng", variant="default")

        yield Footer()

    def _selected_difficulty(self) -> str:
        index = self.query_one("#difficulty_set", RadioSet).pressed_index
        return [DIFFICULTY_EASY, DIFFICULTY_INTERMEDIATE, DIFFICULTY_DIFFICULT][index]

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn_back_ng":
            self.action_go_back()
            return

        if event.button.id == "btn_start":
            name = self.query_one("#player_input", Input).value.strip()
            if not name:
                self.app.notify("Veuillez saisir un nom de joueur.", severity="error")
                return

            difficulty = self._selected_difficulty()
            labels = {
                DIFFICULTY_EASY: "Facile",
                DIFFICULTY_INTERMEDIATE: "Intermédiaire",
                DIFFICULTY_DIFFICULT: "Difficile",
            }
            self.app.notify(
                f"Partie lancée pour {name}  ·  niveau {labels[difficulty]}",
                title="C'est parti !",
            )
            # TODO: pousser GameScreen
            # from src.game.player import Player
            # from src.data.grid_loader import load_random_grid
            # from src.game.game_session import GameSession
            # from src.ui.screens.game_screen import GameScreen
            # session = GameSession(Player(name), difficulty, load_random_grid(difficulty))
            # self.app.push_screen(GameScreen(session))

    def action_go_back(self) -> None:
        self.app.pop_screen()
