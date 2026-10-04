from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame

from constants import *
from save_data import SaveSlot
from screens.menu import MenuScreen
from screens.game import GameScreen
from core.transition import FadeTransition


class Game:
    def __init__(self):
        pygame.init()

        self.screen_flags = pygame.RESIZABLE if Screen.RESIZABLE else 0

        self.logical_screen = pygame.Surface(
            (Screen.WIDTH, Screen.HEIGHT)
        )

        self.screen = pygame.display.set_mode(
            (Screen.WIDTH, Screen.HEIGHT),
            self.screen_flags
        )

        pygame.display.set_caption(Screen.TITLE)

        self.clock = pygame.time.Clock()
        self.running = True

        self.fonts: dict[FontType, pygame.font.Font] = {
            font_type: pygame.font.Font(Font.PATH, font_size)
            for font_type, font_size in Font.SIZES.items()
        }

        self.screens = {
            ScreenState.MAIN: MenuScreen(self.fonts),
            ScreenState.GAME: GameScreen(self.fonts),
        }

        self.current_state = ScreenState.MAIN
        self.current_screen = self.screens[self.current_state]

        self.transition = FadeTransition(
            Screen.WIDTH,
            Screen.HEIGHT,
            duration=Screen.FADE_DURATION_MS / 1000
        )

        self.mouse_pos = (-1, -1)

    def run(self):
        while self.running:
            dt = self.clock.tick(Screen.FPS) / 1000.0

            self.handle_events()
            self.update(dt)
            self.draw()

        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False
                continue

            if event.type == pygame.VIDEORESIZE:
                self.screen = pygame.display.set_mode(
                    event.size,
                    pygame.RESIZABLE
                )
                continue

            if event.type == pygame.MOUSEMOTION:
                mouse_pos = self.transform_mouse_pos(event.pos)

                if mouse_pos is None:
                    mouse_pos = (-1, -1)

                self.current_screen.set_mouse_pos(mouse_pos)

            elif event.type in (
                pygame.MOUSEBUTTONDOWN,
                pygame.MOUSEBUTTONUP
            ):
                mouse_pos = self.transform_mouse_pos(event.pos)

                if mouse_pos is None:
                    continue

                event.pos = mouse_pos

            result = self.current_screen.handle_event(event)

            if result is not None:
                if isinstance(result, tuple):
                    state, slot = result
                else:
                    state, slot = result, None
                self.change_screen(state, slot)

    def update(self, dt: float):
        self.current_screen.update(dt)
        self.transition.update(dt)

    def draw(self):
        self.logical_screen.fill(Color.BACKGROUND.value)

        self.current_screen.draw(self.logical_screen)
        self.transition.draw(self.logical_screen)

        window_width, window_height = self.screen.get_size()

        scale = min(
            window_width / Screen.WIDTH,
            window_height / Screen.HEIGHT
        )

        render_width = int(Screen.WIDTH * scale)
        render_height = int(Screen.HEIGHT * scale)

        offset_x = (window_width - render_width) // 2
        offset_y = (window_height - render_height) // 2

        scaled = pygame.transform.smoothscale(
            self.logical_screen,
            (render_width, render_height)
        )

        self.screen.fill(Color.BLACK.value)
        self.screen.blit(
            scaled,
            (offset_x, offset_y)
        )

        pygame.display.flip()

    def change_screen(self, state: ScreenState, slot: SaveSlot | None = None):
        if state == self.current_state:
            return

        if self.transition.active:
            return

        self.transition.start(
            lambda: self._set_screen(state, slot)
        )

    def _set_screen(self, state: ScreenState, slot: SaveSlot | None = None):
        if state == ScreenState.EXIT:
            self.running = False
            return

        self.current_state = state
        self.current_screen = self.screens[state]

        if state == ScreenState.GAME and slot is not None:
            self.current_screen.open_slot(slot)

    def transform_mouse_pos(self, pos):
        window_width, window_height = self.screen.get_size()

        scale = min(
            window_width / Screen.WIDTH,
            window_height / Screen.HEIGHT
        )

        render_width = Screen.WIDTH * scale
        render_height = Screen.HEIGHT * scale

        offset_x = (window_width - render_width) / 2
        offset_y = (window_height - render_height) / 2

        x, y = pos

        # 게임 화면 밖
        if (
            x < offset_x
            or x >= offset_x + render_width
            or y < offset_y
            or y >= offset_y + render_height
        ):
            return None

        return (
            int((x - offset_x) / scale),
            int((y - offset_y) / scale)
        )