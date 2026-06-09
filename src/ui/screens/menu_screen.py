from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Button, Label, Static


class MenuScreen(Screen):
    """Main menu: new game, resume, scores, rules, credits, quit."""

    def compose(self) -> ComposeResult:
        yield Static("SUDOKU", id="title")
        yield Button("New Game", id="btn_new_game")
        yield Button("Resume", id="btn_resume")
        yield Button("Scores", id="btn_scores")
        yield Button("Rules", id="btn_rules")
        yield Button("Credits", id="btn_credits")
        yield Button("Quit", id="btn_quit", variant="error")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn_quit":
            self.app.exit()
        # Other buttons will push the corresponding screens once implemented
