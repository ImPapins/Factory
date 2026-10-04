from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame

from constants import Color, FontType, ScreenState
from screens.base import BaseScreen
from save_data import SaveSlot, load_save, save_game

class GameScreen(BaseScreen):
    def __init__(self, fonts: dict[FontType, pygame.font.Font]):
        super().__init__(fonts)
        self.current_slot: SaveSlot | None = None
        self.save_data = None
        self.show_settings = False
        self.settings_button = pygame.Rect(0, 0, 120, 48)
        self.save_button = pygame.Rect(0, 0, 180, 52)
        self.main_button = pygame.Rect(0, 0, 180, 52)
        self.saved_message_until = 0

    def open_slot(self, slot: SaveSlot):
        self.current_slot = slot
        self.save_data = load_save(slot)
        self.show_settings = False

    def update_layout(self, surface):
        layout_key = surface.get_size()

        if layout_key == self._layout_key:
            return

        self._layout_key = layout_key

        width, _ = surface.get_size()
        self.settings_button.topright = (width - 24, 24)
        self.save_button.topright = (width - 24, 88)
        self.main_button.topright = (width - 24, 150)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.settings_button.collidepoint(event.pos):
                self.show_settings = not self.show_settings
                return None

            if self.show_settings:
                if self.save_button.collidepoint(event.pos):
                    if self.current_slot is not None and self.save_data is not None:
                        save_game(self.current_slot, self.save_data)
                        self.saved_message_until = pygame.time.get_ticks() + 1500
                    return None

                if self.main_button.collidepoint(event.pos):
                    if self.current_slot is not None and self.save_data is not None:
                        save_game(self.current_slot, self.save_data)
                    return ScreenState.MAIN

        return None

    def draw(self, surface):
        width, height = surface.get_size()
        self.update_layout(surface)
        surface.fill(Color.GAME_BACKGROUND.value)

        if self.current_slot is not None:
            self.draw_text(surface, self.current_slot.name, (width // 2, height // 2))

        settings_color = (
            Color.PANEL_HOVER.value
            if self.settings_button.collidepoint(self.mouse_pos)
            else Color.PANEL.value
        )
        pygame.draw.rect(surface, settings_color, self.settings_button, border_radius=8)
        pygame.draw.rect(surface, Color.BLACK.value, self.settings_button, 2, border_radius=8)
        self.draw_text(surface, "Settings", self.settings_button.center)

        if self.show_settings:
            save_color = Color.PANEL_HOVER.value if self.save_button.collidepoint(self.mouse_pos) else Color.PANEL.value
            main_color = Color.PANEL_HOVER.value if self.main_button.collidepoint(self.mouse_pos) else Color.PANEL.value

            pygame.draw.rect(surface, save_color, self.save_button, border_radius=8)
            pygame.draw.rect(surface, Color.BLACK.value, self.save_button, 2, border_radius=8)
            self.draw_text(surface, "Save", self.save_button.center)

            pygame.draw.rect(surface, main_color, self.main_button, border_radius=8)
            pygame.draw.rect(surface, Color.BLACK.value, self.main_button, 2, border_radius=8)
            self.draw_text(surface, "Main Menu", self.main_button.center)

        if pygame.time.get_ticks() < self.saved_message_until:
            self.draw_text(surface, "Saved", (width // 2, height // 2 + 60))
