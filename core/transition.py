import pygame

from enum import Enum, auto
from constants import Color

class TransitionState(Enum):
    IDLE = auto()
    FADE_OUT = auto()
    FADE_IN = auto()

class FadeTransition:
    def __init__(
        self,
        width: int,
        height: int,
        duration: float = 0.3
    ):
        self.duration = duration

        self.state = TransitionState.IDLE
        self.elapsed = 0.0

        self._on_midpoint = None

        self.surface = pygame.Surface((width, height))
        self.surface.fill(Color.BLACK.value)

    @property
    def active(self) -> bool:
        return self.state != TransitionState.IDLE

    def start(self, on_midpoint=None):
        if self.active:
            return

        self.state = TransitionState.FADE_OUT
        self.elapsed = 0.0
        self._on_midpoint = on_midpoint

    def update(self, dt: float):
        if not self.active:
            return

        self.elapsed += dt

        if self.elapsed < self.duration:
            return

        self.elapsed = 0.0

        if self.state == TransitionState.FADE_OUT:
            self.state = TransitionState.FADE_IN

            if self._on_midpoint:
                self._on_midpoint()
                self._on_midpoint = None

        elif self.state == TransitionState.FADE_IN:
            self.state = TransitionState.IDLE

    def draw(self, screen: pygame.Surface):
        if not self.active:
            return

        progress = min(self.elapsed / self.duration, 1.0)

        if self.state == TransitionState.FADE_OUT:
            alpha = int(progress * 255)
        else:
            alpha = int((1.0 - progress) * 255)

        self.surface.set_alpha(alpha)
        screen.blit(self.surface, (0, 0))