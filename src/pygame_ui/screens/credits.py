import pygame
from src.pygame_ui.app import Screen, W, H
from src.pygame_ui import colors as C
from src.pygame_ui.components import Button, ScrollableText

_CREDITS = [
    "## Projet",
    "Sudoku Python — ESIEE-IT  ·  M1 ILMSI  ·  2025-2026",
    "",
    "## Équipe",
    "- Kevin MAUBLANC",
    "- Mathis PEZERON",
    "- Clément BERDAH",
    "",
    "## Encadrante",
    "Elisabeth Rendler",
    "",
    "## Technologies",
    "- Python 3.12",
    "- Pygame — interface graphique",
    "- Textual — interface terminal (version originale)",
    "- Matplotlib — visualisation des scores",
    "- JSON — persistance des données",
    "",
    "## Architecture",
    "Le projet suit une architecture MVC stricte :",
    "- src/game/   — logique métier (Board, GameSession, IASolver)",
    "- src/data/   — persistance (grilles, scores, sauvegarde)",
    "- src/pygame_ui/ — interface graphique Pygame",
    "",
    "## Licence",
    "Projet académique — Usage éducatif uniquement.",
]


class CreditsScreen(Screen):
    def __init__(self, app):
        super().__init__(app)
        self._scroll_text = ScrollableText(
            (60, 72, W - 120, H - 150), _CREDITS, app.fonts["normal"], line_height=30
        )
        self._btn_back = Button((W // 2 - 120, H - 64, 240, 44), "← Retour", app.fonts["btn"])

    def handle_event(self, event):
        self._scroll_text.handle_event(event)
        if self._btn_back.handle_event(event):
            self.app.pop()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.app.pop()

    def draw(self, surface):
        self.app.draw_header(surface, "Crédits", "ESIEE-IT Sudoku")
        self._scroll_text.draw(surface)
        self._btn_back.draw(surface)
        self.app.draw_footer(surface, "Molette / ↑↓ pour défiler  ·  Échap pour revenir")
