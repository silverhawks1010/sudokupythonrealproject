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

            yield Label("Mode de jeu :", classes="field-label")
            with RadioSet(id="mode_set"):
                yield RadioButton("Joueur humain", id="radio_human", value=True)
                yield RadioButton("IA Joueur",     id="radio_ia")

            with Horizontal(id="btn_row"):
                yield Button("Commencer", id="btn_start",   variant="success")
                yield Button("Retour",    id="btn_back_ng", variant="default")

        yield Footer()

    def _selected_difficulty(self) -> str:
        index = self.query_one("#difficulty_set", RadioSet).pressed_index
        return [DIFFICULTY_EASY, DIFFICULTY_INTERMEDIATE, DIFFICULTY_DIFFICULT][index]

    def _is_ia_mode(self) -> bool:
        return self.query_one("#mode_set", RadioSet).pressed_index == 1

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
            is_ia = self._is_ia_mode()
            labels = {
                DIFFICULTY_EASY: "Facile",
                DIFFICULTY_INTERMEDIATE: "Intermédiaire",
                DIFFICULTY_DIFFICULT: "Difficile",
            }
            mode_label = "IA Joueur" if is_ia else "Joueur humain"
            self.app.notify(
                f"Partie lancée pour {name}  ·  niveau {labels[difficulty]}  ·  {mode_label}",
                title="C'est parti !",
            )

            from src.game.player import Player
            from src.data.grid_loader import load_random_grid
            from src.game.game_session import GameSession
            from src.ui.screens.game_screen import GameScreen

            session = GameSession(
                Player(name), difficulty, load_random_grid(difficulty), is_ia=is_ia
            )
            self.app.push_screen(GameScreen(session))

    def action_go_back(self) -> None:
        self.app.pop_screen()
