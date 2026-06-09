from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Center, Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Button, Static

TITLE_ART = """\
 ███████╗██╗   ██╗██████╗  ██████╗ ██╗  ██╗██╗   ██╗
 ██╔════╝██║   ██║██╔══██╗██╔═══██╗██║ ██╔╝██║   ██║
 ███████╗██║   ██║██║  ██║██║   ██║█████╔╝ ██║   ██║
 ╚════██║██║   ██║██║  ██║██║   ██║██╔═██╗ ██║   ██║
 ███████║╚██████╔╝██████╔╝╚██████╔╝██║  ██╗╚██████╔╝
 ╚══════╝ ╚═════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝ ╚═════╝"""


class MenuScreen(Screen):
    """Menu principal."""

    BINDINGS = [Binding("q", "quit_game", "Quitter")]

    def compose(self) -> ComposeResult:
        yield Static("ESIEE-IT  ·  M1 ILMSI  ·  2025-2026", id="menu_footer")

        with Center():
            with Vertical(id="menu_card"):
                yield Static(TITLE_ART, id="ascii_title")

                yield Button("Nouvelle Partie", id="btn_new_game", variant="success")

                with Horizontal(classes="btn-row"):
                    yield Button("Scores", id="btn_scores", variant="default")
                    yield Button("Règles", id="btn_rules",  variant="default")

                with Horizontal(classes="btn-row"):
                    yield Button("Crédits", id="btn_credits", variant="default")
                    yield Button("Quitter",  id="btn_quit",    variant="error")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        from src.ui.screens.new_game_screen import NewGameScreen
        from src.ui.screens.scores_screen import ScoresScreen
        from src.ui.screens.rules_screen import RulesScreen
        from src.ui.screens.credits_screen import CreditsScreen

        match event.button.id:
            case "btn_new_game":
                self.app.push_screen(NewGameScreen())
            case "btn_scores":
                self.app.push_screen(ScoresScreen())
            case "btn_rules":
                self.app.push_screen(RulesScreen())
            case "btn_credits":
                self.app.push_screen(CreditsScreen())
            case "btn_quit":
                self.app.exit()

    def action_quit_game(self) -> None:
        self.app.exit()
