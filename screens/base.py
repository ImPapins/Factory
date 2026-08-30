import pygame

from constants import Color, FontType, TransitionParam
from typing import Any

class BaseScreen:
    def __init__(self, fonts: dict[FontType, pygame.font.Font]):
        self.fonts = fonts
        self.mouse_pos = (-1, -1)

    def set_mouse_pos(self, pos):
        self.mouse_pos = pos

    def on_enter(self, params: dict[TransitionParam, Any] | None = None):
        """화면으로 진입할 때 호출 (데이터 전달 및 상태 초기화)"""
        pass

    def on_exit(self):
        """화면을 벗어날 때 호출 (정리 작업)"""
        pass

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