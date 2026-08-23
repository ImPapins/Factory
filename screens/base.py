import pygame

from constants import Color, FontType

class BaseScreen:
    def __init__(self, fonts: dict[FontType, pygame.font.Font]):
        self.fonts = fonts
        self.mouse_pos = (-1, -1)

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
        image = self.fonts[font_type].render(text, True, color)
        rect = image.get_rect(center=center)
        surface.blit(image, rect)