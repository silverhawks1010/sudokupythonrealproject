from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import Screen
from textual.widgets import Button, Footer, MarkdownViewer

RULES_TEXT = """\
# Règles du Sudoku

## Objectif
Remplir entièrement la grille **9×9** avec les chiffres **1 à 9** sans jamais répéter
un chiffre dans la même **ligne**, la même **colonne** ou le même **carré 3×3**.

## Grille de départ
La grille de départ comporte déjà des chiffres pré-remplis :
- **Facile** : beaucoup de chiffres déjà placés.
- **Intermédiaire** : quelques chiffres placés.
- **Difficile** : très peu de chiffres placés.

## Saisie d'un nombre
1. Entrez le **numéro de ligne** (1–9).
2. Entrez la **lettre de colonne** (A–I).
3. Entrez la **valeur** à placer (1–9).

Le nombre est placé s'il respecte les règles, sinon un message d'erreur s'affiche.

## Effacer une case
Tapez **C** avant votre saisie pour effacer un nombre que vous avez posé.
_(Les cases pré-remplies ne peuvent pas être modifiées.)_

## Pause
Appuyez sur **P** pour mettre la partie en pause.
La partie est sauvegardée et peut être reprise depuis le menu principal.
_(Aucun score n'est attribué lors d'une pause.)_

## Interruption
Appuyez sur **I** pour interrompre définitivement la partie.
La partie n'est **pas** sauvegardée et un score **négatif** est appliqué :

| Niveau        | Score d'interruption |
|---------------|----------------------|
| Facile        | −1                   |
| Intermédiaire | −2                   |
| Difficile     | −3                   |

## Scores de victoire
Terminer une grille complète rapporte :

| Niveau        | Score de victoire |
|---------------|-------------------|
| Facile        | +2                |
| Intermédiaire | +4                |
| Difficile     | +8                |
"""

class RulesScreen(Screen):
    """Affiche les règles du jeu."""

    BINDINGS = [Binding("escape", "go_back", "Retour")]

    def compose(self) -> ComposeResult:
        yield MarkdownViewer(RULES_TEXT, show_table_of_contents=False)
        yield Button("← Retour", id="btn_back", variant="default")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn_back":
            self.action_go_back()

    def action_go_back(self) -> None:
        self.app.pop_screen()
