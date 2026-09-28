import pygame
from src.pygame_ui import colors as C


class Button:
    def __init__(self, rect, text, font,
                 bg=None, hover_bg=None, text_color=None,
                 border_color=None, border_radius=8, danger=False):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.bg = bg or (C.BTN_DANGER if danger else C.BTN_BG)
        self.hover_bg = hover_bg or (C.BTN_DANGER_HOV if danger else C.BTN_HOVER)
        self.text_color = text_color or C.BTN_TEXT
        self.border_color = border_color or (C.BTN_DANGER_HOV if danger else C.ACCENT_DIM)
        self.border_radius = border_radius
        self._hovered = False

    def handle_event(self, event) -> bool:
        if event.type == pygame.MOUSEMOTION:
            self._hovered = self.rect.collidepoint(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

    def draw(self, surface):
        color = self.hover_bg if self._hovered else self.bg
        pygame.draw.rect(surface, color, self.rect, border_radius=self.border_radius)
        pygame.draw.rect(surface, self.border_color, self.rect, 2, border_radius=self.border_radius)
        surf = self.font.render(self.text, True, self.text_color)
        surface.blit(surf, surf.get_rect(center=self.rect.center))


class TextInput:
    def __init__(self, rect, font, placeholder="", max_length=24):
        self.rect = pygame.Rect(rect)
        self.font = font
        self.placeholder = placeholder
        self.max_length = max_length
        self.text = ""
        self.active = False
        self._blink = True
        self._timer = 0

    def handle_event(self, event) -> bool:
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key not in (pygame.K_RETURN, pygame.K_TAB, pygame.K_ESCAPE):
                if len(self.text) < self.max_length and event.unicode.isprintable():
                    self.text += event.unicode
        return False

    def update(self, dt):
        self._timer += dt
        if self._timer >= 530:
            self._blink = not self._blink
            self._timer = 0

    def draw(self, surface):
        bg = C.INPUT_ACTIVE if self.active else C.INPUT_BG
        border = C.INPUT_BACTIVE if self.active else C.INPUT_BORDER
        pygame.draw.rect(surface, bg, self.rect, border_radius=6)
        pygame.draw.rect(surface, border, self.rect, 2, border_radius=6)

        pad = 10
        if self.text:
            surf = self.font.render(self.text, True, C.TEXT)
            cx = self.rect.x + pad + surf.get_width()
            surface.blit(surf, (self.rect.x + pad, self.rect.centery - surf.get_height() // 2))
        else:
            if not self.active:
                ph = self.font.render(self.placeholder, True, C.TEXT_DIM)
                surface.blit(ph, (self.rect.x + pad, self.rect.centery - ph.get_height() // 2))
            cx = self.rect.x + pad

        if self.active and self._blink:
            ch = self.font.get_height() - 4
            cy = self.rect.centery - ch // 2
            pygame.draw.line(surface, C.TEXT, (cx + 1, cy), (cx + 1, cy + ch), 2)


class RadioGroup:
    def __init__(self, x, y, options, font, selected=0, gap=44):
        self.x = x
        self.y = y
        self.options = options
        self.font = font
        self.selected = selected
        self.gap = gap
        self._centers = [(x + 9, y + i * gap + 9) for i in range(len(options))]

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i, (cx, cy) in enumerate(self._centers):
                hit = pygame.Rect(cx - 14, cy - 14, 220, 28)
                if hit.collidepoint(event.pos):
                    self.selected = i
        return False

    def draw(self, surface):
        for i, ((cx, cy), label) in enumerate(zip(self._centers, self.options)):
            active = (i == self.selected)
            pygame.draw.circle(surface, C.ACCENT_DIM, (cx, cy), 9)
            inner_color = C.ACCENT if active else C.BG_CARD
            pygame.draw.circle(surface, inner_color, (cx, cy), 6)
            ring_color = C.BORDER_THICK if active else C.BORDER_THIN
            pygame.draw.circle(surface, ring_color, (cx, cy), 9, 2)
            color = C.TEXT if active else C.TEXT_DIM
            surf = self.font.render(label, True, color)
            surface.blit(surf, (cx + 16, cy - surf.get_height() // 2))


class ScrollableText:
    """Displays multi-line text with mouse-wheel / arrow-key scrolling."""

    def __init__(self, rect, lines, font, line_height=26):
        self.rect = pygame.Rect(rect)
        self.lines = lines
        self.font = font
        self.line_height = line_height
        self.scroll = 0
        self._max_scroll = max(0, len(lines) * line_height - rect[3])

    def handle_event(self, event):
        if event.type == pygame.MOUSEWHEEL:
            self.scroll = max(0, min(self._max_scroll, self.scroll - event.y * 30))
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.scroll = max(0, self.scroll - 30)
            if event.key == pygame.K_DOWN:
                self.scroll = min(self._max_scroll, self.scroll + 30)

    def draw(self, surface):
        clip = surface.get_clip()
        surface.set_clip(self.rect)
        y = self.rect.y - self.scroll
        for line in self.lines:
            if y + self.line_height > self.rect.y and y < self.rect.bottom:
                if line.startswith("##"):
                    txt = line.lstrip("#").strip()
                    surf = self.font.render(txt, True, C.ACCENT_HOVER)
                elif line.startswith("- "):
                    txt = "•  " + line[2:]
                    surf = self.font.render(txt, True, C.TEXT)
                    surface.blit(surf, (self.rect.x + 16, y))
                    y += self.line_height
                    continue
                else:
                    surf = self.font.render(line, True, C.TEXT)
                surface.blit(surf, (self.rect.x, y))
            y += self.line_height
        surface.set_clip(clip)

        # Scrollbar
        if self._max_scroll > 0:
            bar_h = max(30, self.rect.height * self.rect.height // (self.rect.height + self._max_scroll))
            bar_y = self.rect.y + int(self.scroll / self._max_scroll * (self.rect.height - bar_h))
            bar_rect = pygame.Rect(self.rect.right - 6, bar_y, 4, bar_h)
            pygame.draw.rect(surface, C.ACCENT_DIM, bar_rect, border_radius=2)
