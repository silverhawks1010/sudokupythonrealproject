import pygame
from src.pygame_ui.app import Screen, W, H
from src.pygame_ui import colors as C
from src.pygame_ui.components import Button, ScrollableText

_RULES = [
    "## Objectif",
    "Remplissez la grille 9×9 de sorte que chaque ligne, chaque",
    "colonne et chaque bloc 3×3 contienne les chiffres de 1 à 9",
    "sans répétition.",
    "",
    "## Commandes (mode humain)",
    "- Flèches  →  Déplacer le curseur",
    "- 1 à 9    →  Placer un chiffre",
    "- 0 / Suppr / Backspace  →  Effacer la case",
    "- P        →  Mettre en pause (sauvegarde la partie)",
    "- I        →  Interrompre (abandon avec pénalité)",
    "- Clic souris  →  Sélectionner une case directement",
    "",
    "## Commandes (mode IA)",
    "- N ou Espace  →  Un pas de résolution",
    "- A            →  Résolution automatique (animation)",
    "",
    "## Difficulté & Scores",
    "- Facile       : +2 pts en cas de victoire, -1 si abandon",
    "- Intermédiaire : +4 pts en cas de victoire, -2 si abandon",
    "- Difficile    : +8 pts en cas de victoire, -3 si abandon",
    "",
    "## Indices visuels",
    "- Case violette foncée  →  chiffre initial (verrouillé)",
    "- Case violet clair     →  chiffre placé par le joueur",
    "- Case surlignée violet →  curseur actif",
    "- Chiffres en jaune     →  même valeur que la case active",
    "- Fond rouge            →  placement invalide",
    "",
    "## Sauvegarde",
    "Appuyez sur P pour sauvegarder et revenir au menu.",
    "La partie reprend depuis le menu principal.",
]


class RulesScreen(Screen):
    def __init__(self, app):
        super().__init__(app)
        self._scroll_text = ScrollableText(
            (60, 72, W - 120, H - 150), _RULES, app.fonts["normal"], line_height=28
        )
        self._btn_back = Button((W // 2 - 120, H - 64, 240, 44), "← Retour", app.fonts["btn"])

    def handle_event(self, event):
        self._scroll_text.handle_event(event)
        if self._btn_back.handle_event(event):
            self.app.pop()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.app.pop()

    def draw(self, surface):
        self.app.draw_header(surface, "Règles du Jeu")
        self._scroll_text.draw(surface)
        self._btn_back.draw(surface)
        self.app.draw_footer(surface, "Molette / ↑↓ pour défiler  ·  Échap pour revenir")
