from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import Screen
from textual.widgets import Button, Footer, MarkdownViewer

CREDITS_TEXT = """\
# Crédits

## Projet d'informatique Python
**ESIEE-IT — M1 ILMSI — Semestre 2 — 2025-2026**

---

## Équipe

| Prénom Nom        | Rôle / Tâches principales |
|-------------------|---------------------------|
| MAUBLANC Kevin    |Lead Developer et UI Designer|
| PEZERON Mathis    | Developpers               |
| BERDAHHH Clément  | Developpers               |

---

## Technologies utilisées

- **Python 3.12**
- **Textual** — interface TUI
- **Matplotlib** — graphique des scores
- **JSON** — persistance des données

---

## Encadrement

*Elisabeth Rendler* — responsable du cours

---

*Bonne chance à toutes et à tous !*
"""

class CreditsScreen(Screen):
    """Affiche les crédits de l'équipe."""

    BINDINGS = [Binding("escape", "go_back", "Retour")]

    def compose(self) -> ComposeResult:
        yield MarkdownViewer(CREDITS_TEXT, show_table_of_contents=False)
        yield Button("← Retour", id="btn_back", variant="default")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn_back":
            self.action_go_back()

    def action_go_back(self) -> None:
        self.app.pop_screen()
