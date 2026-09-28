import pygame
from src.pygame_ui.app import Screen, W, H
from src.pygame_ui import colors as C
from src.pygame_ui.components import Button
from src.data import save_manager

TITLE_LINES = [
    " ███████╗██╗   ██╗██████╗  ██████╗ ██╗  ██╗██╗   ██╗",
    " ██╔════╝██║   ██║██╔══██╗██╔═══██╗██║ ██╔╝██║   ██║",
    " ███████╗██║   ██║██║  ██║██║   ██║█████╔╝ ██║   ██║",
    " ╚════██║██║   ██║██║  ██║██║   ██║██╔═██╗ ██║   ██║",
    " ███████║╚██████╔╝██████╔╝╚██████╔╝██║  ██╗╚██████╔╝",
    " ╚══════╝ ╚═════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ",
]


class MenuScreen(Screen):
    def __init__(self, app):
        super().__init__(app)
        self._build_buttons()

    def _build_buttons(self):
        f = self.app.fonts["btn"]
        bw, bh, bx = 300, 46, W // 2 - 150

        has_save = save_manager.has_save()
        items = [("Nouvelle Partie", "new")]
        if has_save:
            items.append(("Reprendre la partie", "resume"))
        items += [
            ("Scores", "scores"),
            ("Règles", "rules"),
            ("Crédits", "credits"),
            ("Quitter", "quit"),
        ]

        start_y = 340 if not has_save else 310
        gap = 56
        self._buttons: list[tuple[Button, str]] = []
        for i, (label, action) in enumerate(items):
            danger = (action == "quit")
            btn = Button((bx, start_y + i * gap, bw, bh), label, f, danger=danger)
            self._buttons.append((btn, action))

    def handle_event(self, event):
        for btn, action in self._buttons:
            if btn.handle_event(event):
                self._do(action)

    def _do(self, action):
        from src.pygame_ui.screens.new_game import NewGameScreen
        from src.pygame_ui.screens.scores import ScoresScreen
        from src.pygame_ui.screens.rules import RulesScreen
        from src.pygame_ui.screens.credits import CreditsScreen
        from src.pygame_ui.screens.game import GameScreen
        import sys

        if action == "new":
            self.app.push(NewGameScreen(self.app))
        elif action == "resume":
            self._resume_game()
        elif action == "scores":
            self.app.push(ScoresScreen(self.app))
        elif action == "rules":
            self.app.push(RulesScreen(self.app))
        elif action == "credits":
            self.app.push(CreditsScreen(self.app))
        elif action == "quit":
            pygame.quit()
            sys.exit()

    def _resume_game(self):
        from src.pygame_ui.screens.game import GameScreen
        from src.game.board import Board
        from src.game.player import Player
        from src.game.game_session import GameSession

        data = save_manager.read_save()
        player = Player(data["player_name"])
        player.total_score = data["total_score"]

        board = Board()
        initial = data.get("initial_board") or data["board"]
        board.load(initial)

        # Re-place player moves on top of the initial grid
        if "current_board" in data:
            for r in range(9):
                for c in range(9):
                    val = data["current_board"][r][c]
                    if val != 0 and not board.is_locked(r, c):
                        board.place(r, c, val)

        session = GameSession(player, data["difficulty"], board)
        session.resume()
        save_manager.delete_save()
        self.app.push(GameScreen(self.app, session))

    def update(self, dt):
        pass

    def draw(self, surface):
        # ASCII title
        mono = self.app.fonts["mono"]
        total_h = len(TITLE_LINES) * 20
        ty = 130 - total_h // 2
        for i, line in enumerate(TITLE_LINES):
            t = mono.render(line, True, C.ACCENT_HOVER)
            surface.blit(t, (W // 2 - t.get_width() // 2, ty + i * 20))

        # Subtitle
        sub = self.app.fonts["small"].render("ESIEE-IT  ·  M1 ILMSI  ·  2025-2026", True, C.TEXT_DIM)
        surface.blit(sub, (W // 2 - sub.get_width() // 2, ty + len(TITLE_LINES) * 20 + 14))

        # Separator
        sep_y = ty + len(TITLE_LINES) * 20 + 44
        pygame.draw.line(surface, C.BORDER_THIN, (W // 2 - 200, sep_y), (W // 2 + 200, sep_y), 1)

        # Buttons
        for btn, _ in self._buttons:
            btn.draw(surface)

        # Footer
        self.app.draw_footer(surface, "↑↓ Naviguez  ·  Entrée pour sélectionner  ·  F11 Plein écran")
