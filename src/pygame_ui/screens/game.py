import pygame
from src.pygame_ui.app import Screen, W, H
from src.pygame_ui import colors as C
from src.pygame_ui.components import Button
from src.game.game_session import GameSession, SessionState
from src.data import save_manager, score_manager
from src.utils.constants import DIFFICULTY_EASY, DIFFICULTY_INTERMEDIATE, DIFFICULTY_DIFFICULT

# ── Grid geometry ────────────────────────────────────────────────────────────
CELL      = 54       # pixel size of one cell
OUTER     = 3        # outer border width
THICK     = 3        # border between 3×3 boxes
THIN      = 1        # border between cells within a box

# Precompute pixel offsets for each row/col (top-left corner of cell content)
_OFFSETS: list[int] = []
_pos = OUTER
for _i in range(9):
    _OFFSETS.append(_pos)
    if _i < 8:
        _pos += CELL + (THICK if (_i + 1) % 3 == 0 else THIN)

GRID_PX = _OFFSETS[8] + CELL + OUTER   # total grid pixel size (square)

# Where to place the grid on screen
GRID_X = (W - GRID_PX) // 2 + 35      # slightly right to leave room for tracker
GRID_Y = 75

# Number tracker strip (left of grid)
TRACKER_X = GRID_X - 90
TRACKER_Y = GRID_Y + 10

# Difficulty display strings
_DIFF_FR = {
    DIFFICULTY_EASY: "Facile",
    DIFFICULTY_INTERMEDIATE: "Intermédiaire",
    DIFFICULTY_DIFFICULT: "Difficile",
}

# IA auto-play timing
IA_AUTO_INTERVAL = 150   # ms between auto steps


def _cell_rect(row: int, col: int) -> pygame.Rect:
    return pygame.Rect(GRID_X + _OFFSETS[col], GRID_Y + _OFFSETS[row], CELL, CELL)


def _count_digit(board, digit: int) -> int:
    return sum(board.get(r, c) == digit for r in range(9) for c in range(9))


class GameScreen(Screen):
    def __init__(self, app, session: GameSession):
        super().__init__(app)
        self._session   = session
        self._board     = session.board
        self._cursor    = [0, 0]
        self._message   = ""
        self._msg_error = False
        self._msg_timer = 0

        # IA auto-play state
        self._ia_auto   = False
        self._ia_timer  = 0

        # Build buttons
        fbtn = app.fonts["btn"]
        fsmall = app.fonts["small"]
        btn_y = GRID_Y + GRID_PX + 14
        if session.is_ia:
            self._btn_step   = Button((GRID_X, btn_y, 130, 38), "Pas (N)", fsmall)
            self._btn_auto   = Button((GRID_X + 140, btn_y, 130, 38), "Auto (A)", fsmall)
        self._btn_pause     = Button((W - 200, btn_y, 90, 38), "Pause (P)", fsmall,
                                      bg=C.BTN_BG, hover_bg=C.BTN_HOVER)
        self._btn_interrupt = Button((W - 104, btn_y, 100, 38), "Abandon (I)", fsmall, danger=True)

    # ── Events ───────────────────────────────────────────────────────────────
    def handle_event(self, event):
        if self._session.state != SessionState.RUNNING:
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._handle_click(event.pos)

        if event.type == pygame.KEYDOWN:
            self._handle_key(event)

        # Button events
        if self._session.is_ia:
            if self._btn_step.handle_event(event):
                self._ia_step()
            if self._btn_auto.handle_event(event):
                self._ia_auto = not self._ia_auto
        if self._btn_pause.handle_event(event):
            self._pause()
        if self._btn_interrupt.handle_event(event):
            self._interrupt()

    def _handle_click(self, pos):
        for row in range(9):
            for col in range(9):
                if _cell_rect(row, col).collidepoint(pos):
                    self._cursor = [row, col]
                    return

    def _handle_key(self, event):
        k = event.key
        # Movement
        if k == pygame.K_UP:    self._move(-1,  0)
        elif k == pygame.K_DOWN:  self._move(1,   0)
        elif k == pygame.K_LEFT:  self._move(0,  -1)
        elif k == pygame.K_RIGHT: self._move(0,   1)
        # Placement
        elif k in (pygame.K_1, pygame.K_KP1): self._place(1)
        elif k in (pygame.K_2, pygame.K_KP2): self._place(2)
        elif k in (pygame.K_3, pygame.K_KP3): self._place(3)
        elif k in (pygame.K_4, pygame.K_KP4): self._place(4)
        elif k in (pygame.K_5, pygame.K_KP5): self._place(5)
        elif k in (pygame.K_6, pygame.K_KP6): self._place(6)
        elif k in (pygame.K_7, pygame.K_KP7): self._place(7)
        elif k in (pygame.K_8, pygame.K_KP8): self._place(8)
        elif k in (pygame.K_9, pygame.K_KP9): self._place(9)
        elif k in (pygame.K_0, pygame.K_KP0, pygame.K_DELETE, pygame.K_BACKSPACE):
            self._clear()
        # Controls
        elif k == pygame.K_p: self._pause()
        elif k == pygame.K_i: self._interrupt()
        elif k == pygame.K_ESCAPE: self._pause()
        # IA
        elif k in (pygame.K_n, pygame.K_SPACE) and self._session.is_ia:
            self._ia_step()
        elif k == pygame.K_a and self._session.is_ia:
            self._ia_auto = not self._ia_auto

    def _move(self, dr, dc):
        self._cursor[0] = max(0, min(8, self._cursor[0] + dr))
        self._cursor[1] = max(0, min(8, self._cursor[1] + dc))

    def _place(self, value):
        if self._session.is_ia:
            return
        row, col = self._cursor
        if self._board.is_locked(row, col):
            self._set_msg("Case verrouillée (chiffre initial).", error=True)
            return
        ok = self._session.human_place(row, col, value)
        if not ok:
            self._set_msg(f"Impossible de placer {value} ici !", error=True)
        else:
            self._set_msg("")
            if self._session.state == SessionState.WON:
                self._on_win()

    def _clear(self):
        if self._session.is_ia:
            return
        row, col = self._cursor
        if not self._session.human_clear(row, col):
            self._set_msg("Impossible d'effacer cette case.", error=True)
        else:
            self._set_msg("")

    def _ia_step(self):
        move = self._session.ia_step()
        if move is None:
            self._set_msg("Aucun mouvement possible.", error=True)
            self._ia_auto = False
        else:
            r, c, v = move
            self._cursor = [r, c]
            self._set_msg(f"IA → ({r+1},{c+1}) = {v}")
            if self._session.state == SessionState.WON:
                self._on_win()

    def _pause(self):
        self._session.pause()
        data = {
            "player_name":   self._session.player.name,
            "difficulty":    self._session.difficulty,
            "initial_board": self._board.initial_grid(),
            "current_board": self._board.to_list(),
            "total_score":   self._session.player.total_score,
        }
        save_manager.write_save(data)
        self.app.pop()

    def _interrupt(self):
        self._session.interrupt()
        score_manager.save_score(
            self._session.player.name, self._session.player.total_score
        )
        save_manager.delete_save()
        self.app.pop()

    def _on_win(self):
        score_manager.save_score(
            self._session.player.name, self._session.player.total_score
        )
        self._ia_auto = False
        self._show_win_overlay = True

    def _set_msg(self, text, error=False):
        self._message   = text
        self._msg_error = error
        self._msg_timer = 3000

    # ── Update ───────────────────────────────────────────────────────────────
    def __init_extra(self):
        self._show_win_overlay = False

    def update(self, dt):
        if not hasattr(self, "_show_win_overlay"):
            self._show_win_overlay = False

        if self._msg_timer > 0:
            self._msg_timer -= dt
            if self._msg_timer <= 0:
                self._message = ""

        if self._ia_auto and self._session.state == SessionState.RUNNING:
            self._ia_timer += dt
            if self._ia_timer >= IA_AUTO_INTERVAL:
                self._ia_timer = 0
                self._ia_step()

        # Win overlay auto-close after 3 s
        if self._show_win_overlay:
            if not hasattr(self, "_win_timer"):
                self._win_timer = 3500
            self._win_timer -= dt
            if self._win_timer <= 0:
                self._show_win_overlay = False
                self.app.pop()

    # ── Drawing ──────────────────────────────────────────────────────────────
    def draw(self, surface):
        self._draw_header(surface)
        self._draw_grid(surface)
        self._draw_tracker(surface)
        self._draw_message(surface)
        self._draw_buttons(surface)
        self._draw_footer(surface)
        if getattr(self, "_show_win_overlay", False):
            self._draw_win_overlay(surface)

    def _draw_header(self, surface):
        pygame.draw.rect(surface, C.BG_PANEL, (0, 0, W, 60))
        pygame.draw.line(surface, C.BORDER_THICK, (0, 60), (W, 60), 2)

        fn = self.app.fonts["normal"]
        fs = self.app.fonts["sub"]
        p  = self._session.player

        diff_fr  = _DIFF_FR.get(self._session.difficulty, self._session.difficulty)
        mode_str = "IA" if self._session.is_ia else "Humain"

        parts = [
            (f"  {p.name}", C.TEXT),
            ("  |  ", C.TEXT_DIM),
            (f"Score : {p.total_score} pts", C.ACCENT_HOVER),
            ("  |  ", C.TEXT_DIM),
            (diff_fr, C.TEXT_DIM),
            ("  |  ", C.TEXT_DIM),
            (mode_str, C.TEXT_DIM),
        ]
        x = 10
        for txt, col in parts:
            s = fs.render(txt, True, col)
            surface.blit(s, (x, 60 // 2 - s.get_height() // 2))
            x += s.get_width()

    def _draw_grid(self, surface):
        board  = self._board
        cr, cc = self._cursor
        cursor_val = board.get(cr, cc)

        # Outer border rectangle
        outer = pygame.Rect(GRID_X - OUTER, GRID_Y - OUTER, GRID_PX, GRID_PX)
        pygame.draw.rect(surface, C.BORDER_OUTER, outer, border_radius=4)

        for row in range(9):
            for col in range(9):
                rect = _cell_rect(row, col)
                val  = board.get(row, col)
                locked = board.is_locked(row, col)
                is_cursor = (row == cr and col == cc)
                is_match  = (cursor_val != 0 and val == cursor_val and not is_cursor)

                # Background
                if is_cursor:
                    bg = C.CELL_CURSOR
                elif is_match:
                    bg = C.CELL_MATCH
                elif locked:
                    bg = C.CELL_LOCKED
                elif val != 0:
                    bg = C.CELL_PLAYER
                else:
                    bg = C.CELL_EMPTY
                pygame.draw.rect(surface, bg, rect)

                # Same-row / same-col / same-box highlight (subtle)
                if not is_cursor:
                    same_zone = (
                        row == cr or col == cc
                        or (row // 3 == cr // 3 and col // 3 == cc // 3)
                    )
                    if same_zone and not is_match:
                        highlight = pygame.Surface((CELL, CELL), pygame.SRCALPHA)
                        highlight.fill((120, 60, 200, 28))
                        surface.blit(highlight, rect)

                # Number
                if val != 0:
                    if is_cursor:
                        color = C.TEXT_CURSOR
                    elif is_match:
                        color = C.TEXT_MATCH
                    elif locked:
                        color = C.TEXT_LOCKED
                    else:
                        color = C.TEXT_PLAYER
                    num = self.app.fonts["cell"].render(str(val), True, color)
                    surface.blit(num, num.get_rect(center=rect.center))

        # Draw thick box borders (drawn last, on top)
        self._draw_grid_lines(surface)

    def _draw_grid_lines(self, surface):
        # Horizontal lines
        for i in range(10):
            y = GRID_Y - OUTER + (
                _OFFSETS[i] - OUTER if i < 9 else GRID_PX - OUTER
            )
            is_box = (i % 3 == 0)
            w = THICK if is_box else THIN
            col = C.BORDER_THICK if is_box else C.BORDER_THIN
            pygame.draw.line(surface, col,
                             (GRID_X - OUTER, y),
                             (GRID_X - OUTER + GRID_PX, y), w)
        # Vertical lines
        for j in range(10):
            x = GRID_X - OUTER + (
                _OFFSETS[j] - OUTER if j < 9 else GRID_PX - OUTER
            )
            is_box = (j % 3 == 0)
            w = THICK if is_box else THIN
            col = C.BORDER_THICK if is_box else C.BORDER_THIN
            pygame.draw.line(surface, col,
                             (x, GRID_Y - OUTER),
                             (x, GRID_Y - OUTER + GRID_PX), w)

    def _draw_tracker(self, surface):
        board  = self._board
        font   = self.app.fonts["tracker"]
        fsmall = self.app.fonts["small"]

        label = fsmall.render("Chiffres", True, C.TEXT_DIM)
        surface.blit(label, (TRACKER_X, TRACKER_Y - 24))

        step = (GRID_PX - 20) // 9
        for digit in range(1, 10):
            count = _count_digit(board, digit)
            done  = (count >= 9)
            y     = TRACKER_Y + (digit - 1) * step + step // 2 - font.get_height() // 2

            bg_col = C.BG_CARD if not done else C.BG_PANEL
            pygame.draw.rect(surface, bg_col, (TRACKER_X - 2, y - 4, 72, font.get_height() + 8), border_radius=6)

            color = C.TEXT_DIM if done else C.ACCENT_HOVER
            surf  = font.render(str(digit), True, color)
            surface.blit(surf, (TRACKER_X + 8, y))

            cnt_s = fsmall.render(f"{count}/9", True, C.TEXT_DIM if done else C.TEXT_DIM)
            surface.blit(cnt_s, (TRACKER_X + 38, y + font.get_height() // 2 - cnt_s.get_height() // 2))

            if done:
                # Strikethrough
                mid_y = y + font.get_height() // 2
                pygame.draw.line(surface, C.TEXT_DIM, (TRACKER_X - 2, mid_y), (TRACKER_X + 68, mid_y), 2)

    def _draw_message(self, surface):
        if not self._message:
            return
        msg_y = GRID_Y + GRID_PX + 58
        color = C.TEXT_ERROR if self._msg_error else C.TEXT_SUCCESS
        surf  = self.app.fonts["normal"].render(self._message, True, color)
        surface.blit(surf, (GRID_X, msg_y))

    def _draw_buttons(self, surface):
        if self._session.is_ia:
            self._btn_step.draw(surface)
            auto_text = "Stop auto (A)" if self._ia_auto else "Auto (A)"
            self._btn_auto.text = auto_text
            self._btn_auto.draw(surface)
        self._btn_pause.draw(surface)
        self._btn_interrupt.draw(surface)

    def _draw_footer(self, surface):
        if self._session.is_ia:
            hint = "N/Espace → pas IA  ·  A → auto  ·  P → pause  ·  I → abandon"
        else:
            hint = "Flèches → déplacer  ·  1-9 → placer  ·  0/Suppr → effacer  ·  P → pause  ·  I → abandon"
        self.app.draw_footer(surface, hint)

    def _draw_win_overlay(self, surface):
        overlay = pygame.Surface((W, H), pygame.SRCALPHA)
        overlay.fill((10, 5, 22, 210))
        surface.blit(overlay, (0, 0))

        cx, cy = W // 2, H // 2
        box = pygame.Rect(cx - 240, cy - 120, 480, 240)
        pygame.draw.rect(surface, C.BG_CARD, box, border_radius=16)
        pygame.draw.rect(surface, C.ACCENT, box, 3, border_radius=16)

        title = self.app.fonts["heading"].render("Félicitations !", True, C.YELLOW)
        surface.blit(title, title.get_rect(centerx=cx, centery=cy - 60))

        pts = self._session.session_score
        score_txt = self.app.fonts["sub"].render(
            f"+{pts} pts  —  Total : {self._session.player.total_score} pts", True, C.TEXT
        )
        surface.blit(score_txt, score_txt.get_rect(centerx=cx, centery=cy))

        hint = self.app.fonts["small"].render("Retour au menu dans quelques secondes…", True, C.TEXT_DIM)
        surface.blit(hint, hint.get_rect(centerx=cx, centery=cy + 55))
