import sys
import pygame

from src.pygame_ui import colors as C

W, H = 960, 680
FPS  = 60


def _load_fonts():
    candidates = ["segoeui", "calibri", "arial", "freesansbold"]
    name = next((f for f in candidates if pygame.font.match_font(f)), None)
    mono = pygame.font.match_font("consolas") or pygame.font.match_font("couriernew")
    def f(size, bold=False):
        return pygame.font.SysFont(name, size, bold=bold) if name else pygame.font.Font(None, size + 6)
    def fm(size):
        return pygame.font.SysFont(mono, size) if mono else pygame.font.Font(None, size + 6)
    return {
        "title":   f(52, bold=True),
        "heading": f(30, bold=True),
        "sub":     f(22, bold=True),
        "normal":  f(20),
        "small":   f(16),
        "cell":    f(30, bold=True),
        "tracker": f(24, bold=True),
        "mono":    fm(18),
        "btn":     f(20, bold=True),
    }


class Screen:
    def __init__(self, app: "PygameApp"):
        self.app = app

    def handle_event(self, event): pass
    def update(self, dt: int): pass
    def draw(self, surface: pygame.Surface): pass


class PygameApp:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((W, H))
        pygame.display.set_caption("Sudoku — ESIEE-IT")
        try:
            icon = pygame.Surface((32, 32))
            icon.fill(C.ACCENT)
            pygame.display.set_icon(icon)
        except Exception:
            pass
        self.clock = pygame.time.Clock()
        self.fonts = _load_fonts()
        self._stack: list[Screen] = []

    # ── Navigation ──────────────────────────────────────────────────────────
    def push(self, screen: Screen):
        self._stack.append(screen)

    def pop(self):
        if len(self._stack) > 1:
            self._stack.pop()

    def replace(self, screen: Screen):
        if self._stack:
            self._stack[-1] = screen
        else:
            self._stack.append(screen)

    @property
    def current(self) -> Screen | None:
        return self._stack[-1] if self._stack else None

    # ── Main loop ────────────────────────────────────────────────────────────
    def run(self):
        from src.pygame_ui.screens.menu import MenuScreen
        self.push(MenuScreen(self))

        while True:
            dt = self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if self.current:
                    self.current.handle_event(event)

            if self.current:
                self.current.update(dt)

            self.surface.fill(C.BG)
            if self.current:
                self.current.draw(self.surface)
            pygame.display.flip()

    # ── Drawing helpers ──────────────────────────────────────────────────────
    def draw_header(self, surface, title, subtitle=""):
        """Standard top bar used by info/static screens."""
        pygame.draw.rect(surface, C.BG_PANEL, (0, 0, W, 58))
        pygame.draw.line(surface, C.BORDER_THICK, (0, 58), (W, 58), 2)
        t = self.fonts["heading"].render(title, True, C.TEXT)
        surface.blit(t, (20, 58 // 2 - t.get_height() // 2))
        if subtitle:
            s = self.fonts["small"].render(subtitle, True, C.TEXT_DIM)
            surface.blit(s, (W - s.get_width() - 20, 58 // 2 - s.get_height() // 2))

    def draw_footer(self, surface, text):
        pygame.draw.rect(surface, C.BG_PANEL, (0, H - 38, W, 38))
        pygame.draw.line(surface, C.BORDER_THIN, (0, H - 38), (W, H - 38), 1)
        s = self.fonts["small"].render(text, True, C.TEXT_DIM)
        surface.blit(s, (W // 2 - s.get_width() // 2, H - 38 + 10))
