import pygame
from src.pygame_ui.app import Screen, W, H
from src.pygame_ui import colors as C
from src.pygame_ui.components import Button
from src.data import score_manager


class ScoresScreen(Screen):
    def __init__(self, app):
        super().__init__(app)
        fbtn = app.fonts["btn"]
        self._btn_chart = Button((W // 2 - 155, H - 120, 150, 44), "Graphique", fbtn)
        self._btn_back  = Button((W // 2 + 5,   H - 120, 150, 44), "← Retour",  fbtn)
        self._scores = sorted(score_manager.load_scores().items(), key=lambda x: -x[1])
        self._best   = score_manager.best_player()
        self._scroll = 0

    def handle_event(self, event):
        if self._btn_back.handle_event(event):
            self.app.pop()
        if self._btn_chart.handle_event(event):
            self._show_chart()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.app.pop()
        if event.type == pygame.MOUSEWHEEL:
            max_s = max(0, len(self._scores) * 48 - (H - 240))
            self._scroll = max(0, min(max_s, self._scroll - event.y * 30))

    def _show_chart(self):
        if not self._scores:
            return
        try:
            import matplotlib.pyplot as plt
            names  = [n for n, _ in self._scores]
            values = [s for _, s in self._scores]
            fig, ax = plt.subplots(figsize=(10, 5))
            fig.patch.set_facecolor("#0a0516")
            ax.set_facecolor("#14072a")
            bars = ax.bar(names, values, color="#7c3aed", edgecolor="#a78bfa")
            for bar, val in zip(bars, values):
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1,
                        str(val), ha="center", va="bottom", color="#e9d5ff", fontsize=10)
            ax.set_title("Scores des joueurs", color="#c678dd", fontsize=14)
            ax.tick_params(colors="#a78bfa")
            ax.spines[:].set_color("#4c1d95")
            plt.tight_layout()
            plt.show()
        except ImportError:
            pass

    def draw(self, surface):
        self.app.draw_header(surface, "Tableau des Scores")

        fnorm = self.app.fonts["normal"]
        fsub  = self.app.fonts["sub"]
        fsmall = self.app.fonts["small"]

        # Best player banner
        if self._best:
            name, score = self._best
            banner = f"🏆  Meilleur joueur : {name}  —  {score} pts"
            b = fsub.render(banner, True, C.YELLOW)
            bx = W // 2 - b.get_width() // 2
            pygame.draw.rect(surface, C.BG_CARD, (bx - 16, 72, b.get_width() + 32, 38), border_radius=8)
            surface.blit(b, (bx, 79))
        else:
            no = fnorm.render("Aucun score enregistré.", True, C.TEXT_DIM)
            surface.blit(no, (W // 2 - no.get_width() // 2, 80))

        # Column headers
        hx = W // 2 - 240
        pygame.draw.rect(surface, C.BG_PANEL, (hx, 122, 480, 34))
        surface.blit(fsub.render("#", True, C.TEXT_DIM),   (hx + 12, 128))
        surface.blit(fsub.render("Joueur", True, C.TEXT_DIM), (hx + 52, 128))
        surface.blit(fsub.render("Score", True, C.TEXT_DIM),  (hx + 390, 128))
        pygame.draw.line(surface, C.BORDER_THIN, (hx, 156), (hx + 480, 156), 1)

        # Rows
        table_top, table_bot = 157, H - 140
        clip = surface.get_clip()
        surface.set_clip(pygame.Rect(hx, table_top, 480, table_bot - table_top))

        for rank, (name, score) in enumerate(self._scores, 1):
            ry = table_top + (rank - 1) * 48 - self._scroll
            if ry + 48 < table_top or ry > table_bot:
                continue
            row_bg = C.BG_CARD if rank % 2 == 0 else C.BG_PANEL
            pygame.draw.rect(surface, row_bg, (hx, ry, 480, 46))
            rc = C.YELLOW if rank == 1 else (C.ACCENT_HOVER if rank == 2 else (C.TEXT_DIM if rank == 3 else C.TEXT_DIM))
            surface.blit(fnorm.render(str(rank), True, rc), (hx + 12, ry + 13))
            surface.blit(fnorm.render(name, True, C.TEXT), (hx + 52, ry + 13))
            pts = fnorm.render(f"{score} pts", True, C.ACCENT_HOVER)
            surface.blit(pts, (hx + 480 - pts.get_width() - 12, ry + 13))

        surface.set_clip(clip)
        pygame.draw.line(surface, C.BORDER_THIN, (hx, table_bot), (hx + 480, table_bot), 1)

        self._btn_chart.draw(surface)
        self._btn_back.draw(surface)
        self.app.draw_footer(surface, "Molette pour défiler  ·  Échap pour revenir")
