import pygame

from constants import Color, FontType

class BaseScreen:
    _TEXT_CACHE_MAX = 512

    def __init__(self, fonts: dict[FontType, pygame.font.Font]):
        self.fonts = fonts
        self.mouse_pos = (-1, -1)
        self._layout_key = None
        self._text_cache = {}

    def set_mouse_pos(self, pos):
        self.mouse_pos = pos

    def handle_event(self, event):
        return None

    def update(self, dt):
        return None

    def draw_text(
        self,
        surface,
        text,
        center,
        color=Color.WHITE.value,
        font_type=FontType.BODY,
    ):
        key = (text, tuple(color), font_type)
        image = self._text_cache.get(key)

        if image is None:
            image = self.fonts[font_type].render(text, True, color)

            if len(self._text_cache) >= self._TEXT_CACHE_MAX:
                self._text_cache.pop(next(iter(self._text_cache)))

            self._text_cache[key] = image

        rect = image.get_rect(center=center)
        surface.blit(image, rect)