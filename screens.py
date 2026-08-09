import pygame

from constants import Color, FontType, GameState
from save_data import SaveSlot, delete_save, ensure_save, get_save_slots, load_save, save_game


class BaseScreen:
    def __init__(self, fonts: dict[FontType, pygame.font.Font]):
        self.fonts = fonts

    def handle_event(self, event):
        return None

    def update(self):
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


class MainScreen(BaseScreen):
    def __init__(self, fonts: dict[FontType, pygame.font.Font]):
        super().__init__(fonts)
        self.slots = get_save_slots()
        self.slot_buttons: dict[int, pygame.Rect] = {}
        self.delete_button = pygame.Rect(0, 0, 180, 56)
        self.play_button = pygame.Rect(0, 0, 240, 56)
        self.quit_button = pygame.Rect(0, 0, 180, 56)
        self.selected_slot: SaveSlot | None = None
        self.confirm_delete = False

    def update_layout(self, surface):
        width, height = surface.get_size()
        button_width = min(420, width - 80)
        button_height = 64
        start_y = height // 2 - 40

        self.slot_buttons = {}
        for offset, slot in enumerate(self.slots):
            rect = pygame.Rect(0, 0, button_width, button_height)
            rect.center = (width // 2, start_y + offset * 84)
            self.slot_buttons[slot.index] = rect

        action_y = height - 80
        self.delete_button.center = (width // 2 - 120, action_y)
        self.play_button.center = (width // 2 + 120, action_y)

        if self.selected_slot is not None and not self.selected_slot.exists:
            self.play_button.center = (width // 2, action_y)

        self.quit_button.bottomright = (width - 24, height - 24)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for slot in self.slots:
                if self.slot_buttons.get(slot.index, pygame.Rect(0, 0, 0, 0)).collidepoint(event.pos):
                    self.selected_slot = slot
                    self.confirm_delete = False
                    return None

            if self.selected_slot is not None:
                if self.selected_slot.exists and self.delete_button.collidepoint(event.pos):
                    if self.confirm_delete:
                        delete_save(self.selected_slot)
                        self.slots = get_save_slots()
                        self.selected_slot = None
                        self.confirm_delete = False
                    else:
                        self.confirm_delete = True
                    return None

                if self.play_button.collidepoint(event.pos):
                    ensure_save(self.selected_slot)
                    self.slots = get_save_slots()
                    return GameState.GAME

            if self.quit_button.collidepoint(event.pos):
                return GameState.EXIT

        return None

    def draw(self, surface):
        width, height = surface.get_size()
        self.update_layout(surface)
        mouse_pos = pygame.mouse.get_pos()

        surface.fill(Color.BACKGROUND.value)
        self.draw_text(surface, "Automation Factory", (width // 2, 110), font_type=FontType.TITLE)
        self.draw_text(surface, "Choose a save slot", (width // 2, 170))

        for slot in self.slots:
            rect = self.slot_buttons[slot.index]
            color = Color.PANEL_HOVER.value if rect.collidepoint(mouse_pos) else Color.PANEL.value
            label = f"{slot.name} - {'Continue' if slot.exists else 'New Factory'}"
            border_color = Color.ACCENT.value

            if self.selected_slot is not None and self.selected_slot.index == slot.index:
                border_color = Color.WHITE.value

            pygame.draw.rect(surface, color, rect, border_radius=8)
            pygame.draw.rect(surface, border_color, rect, 3, border_radius=8)
            self.draw_text(surface, label, rect.center)

        if self.selected_slot is not None:
            delete_color = (
                Color.DANGER_HOVER.value
                if self.delete_button.collidepoint(mouse_pos)
                else Color.DANGER.value
            )
            play_color = (
                Color.PANEL_HOVER.value
                if self.play_button.collidepoint(mouse_pos)
                else Color.ACCENT.value
            )
            play_label = "Continue" if self.selected_slot.exists else "New Factory"
            delete_label = "Confirm Delete" if self.confirm_delete else "Delete Slot"

            self.draw_text(surface, f"Selected: {self.selected_slot.name}", (width // 2, height - 140))
            if self.selected_slot.exists:
                pygame.draw.rect(surface, delete_color, self.delete_button, border_radius=8)
                pygame.draw.rect(surface, Color.BLACK.value, self.delete_button, 2, border_radius=8)
                self.draw_text(surface, delete_label, self.delete_button.center)
            pygame.draw.rect(surface, play_color, self.play_button, border_radius=8)
            pygame.draw.rect(surface, Color.BLACK.value, self.play_button, 2, border_radius=8)
            self.draw_text(surface, play_label, self.play_button.center, Color.BLACK.value)

        quit_color = Color.PANEL_HOVER.value if self.quit_button.collidepoint(mouse_pos) else Color.PANEL.value
        pygame.draw.rect(surface, quit_color, self.quit_button, border_radius=8)
        pygame.draw.rect(surface, Color.ACCENT.value, self.quit_button, 2, border_radius=8)
        self.draw_text(surface, "Quit Game", self.quit_button.center)


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
                    return GameState.MAIN

        return None

    def draw(self, surface):
        width, height = surface.get_size()
        self.update_layout(surface)
        mouse_pos = pygame.mouse.get_pos()
        surface.fill(Color.GAME_BACKGROUND.value)

        if self.current_slot is not None:
            self.draw_text(surface, self.current_slot.name, (width // 2, height // 2))

        settings_color = (
            Color.PANEL_HOVER.value
            if self.settings_button.collidepoint(mouse_pos)
            else Color.PANEL.value
        )
        pygame.draw.rect(surface, settings_color, self.settings_button, border_radius=8)
        pygame.draw.rect(surface, Color.BLACK.value, self.settings_button, 2, border_radius=8)
        self.draw_text(surface, "Settings", self.settings_button.center)

        if self.show_settings:
            save_color = Color.PANEL_HOVER.value if self.save_button.collidepoint(mouse_pos) else Color.PANEL.value
            main_color = Color.PANEL_HOVER.value if self.main_button.collidepoint(mouse_pos) else Color.PANEL.value

            pygame.draw.rect(surface, save_color, self.save_button, border_radius=8)
            pygame.draw.rect(surface, Color.BLACK.value, self.save_button, 2, border_radius=8)
            self.draw_text(surface, "Save", self.save_button.center)

            pygame.draw.rect(surface, main_color, self.main_button, border_radius=8)
            pygame.draw.rect(surface, Color.BLACK.value, self.main_button, 2, border_radius=8)
            self.draw_text(surface, "Main Menu", self.main_button.center)

        if pygame.time.get_ticks() < self.saved_message_until:
            self.draw_text(surface, "Saved", (width // 2, height // 2 + 60))
