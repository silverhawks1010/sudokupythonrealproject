import pygame
from src.pygame_ui.app import Screen, W, H
from src.pygame_ui import colors as C
from src.pygame_ui.components import Button, TextInput, RadioGroup
from src.utils.constants import DIFFICULTY_EASY, DIFFICULTY_INTERMEDIATE, DIFFICULTY_DIFFICULT


_DIFF_LABELS  = ["Facile (+2 pts)", "Intermédiaire (+4 pts)", "Difficile (+8 pts)"]
_DIFF_VALUES  = [DIFFICULTY_EASY, DIFFICULTY_INTERMEDIATE, DIFFICULTY_DIFFICULT]
_MODE_LABELS  = ["Joueur humain", "IA (résolution automatique)"]


class NewGameScreen(Screen):
    def __init__(self, app):
        super().__init__(app)
        f   = app.fonts["normal"]
        fbtn = app.fonts["btn"]

        self._name_input = TextInput((W // 2 - 180, 165, 360, 44), f, placeholder="Votre nom…")
        self._diff_radio = RadioGroup(W // 2 - 140, 258, _DIFF_LABELS, f, selected=0)
        self._mode_radio = RadioGroup(W // 2 - 140, 410, _MODE_LABELS, f, selected=0)

        self._btn_start = Button((W // 2 - 150, 516, 300, 48), "Démarrer", fbtn)
        self._btn_back  = Button((W // 2 - 150, 576, 300, 44), "← Retour", fbtn,
                                  bg=C.BTN_BG, hover_bg=C.BTN_HOVER)
        self._error = ""

    def handle_event(self, event):
        self._name_input.handle_event(event)
        self._diff_radio.handle_event(event)
        self._mode_radio.handle_event(event)

        if self._btn_start.handle_event(event):
            self._start()
        if self._btn_back.handle_event(event):
            self.app.pop()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.app.pop()

    def _start(self):
        name = self._name_input.text.strip()
        if not name:
            self._error = "Veuillez entrer votre nom."
            return
        self._error = ""

        from src.pygame_ui.screens.game import GameScreen
        from src.game.player import Player
        from src.game.game_session import GameSession
        from src.data.grid_loader import load_random_grid

        difficulty = _DIFF_VALUES[self._diff_radio.selected]
        is_ia      = (self._mode_radio.selected == 1)

        board  = load_random_grid(difficulty)
        player = Player(name)
        session = GameSession(player, difficulty, board, is_ia=is_ia)
        self.app.replace(GameScreen(self.app, session))

    def update(self, dt):
        self._name_input.update(dt)

    def draw(self, surface):
        self.app.draw_header(surface, "Nouvelle Partie", "ESIEE-IT Sudoku")
        f   = self.app.fonts["normal"]
        sub = self.app.fonts["sub"]

        def label(text, y):
            s = sub.render(text, True, C.TEXT_DIM)
            surface.blit(s, (W // 2 - 180, y))

        label("Nom du joueur", 138)
        self._name_input.draw(surface)

        label("Difficulté", 228)
        self._diff_radio.draw(surface)

        label("Mode de jeu", 380)
        self._mode_radio.draw(surface)

        if self._error:
            err = f.render(self._error, True, C.TEXT_ERROR)
            surface.blit(err, (W // 2 - err.get_width() // 2, 490))

        self._btn_start.draw(surface)
        self._btn_back.draw(surface)

        self.app.draw_footer(surface, "Entrée pour démarrer  ·  Échap pour revenir")
