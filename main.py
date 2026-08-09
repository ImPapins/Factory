import pygame

from constants import *
from screens import *

pygame.init()

screen_size = (Screen.WIDTH, Screen.HEIGHT)
screen_flags = pygame.RESIZABLE if Screen.RESIZABLE else 0
screen = pygame.display.set_mode(screen_size, screen_flags)
pygame.display.set_caption(Screen.TITLE)
clock = pygame.time.Clock()

fonts: dict[FontType, pygame.font.Font] = {
    font_type: pygame.font.Font(Font.PATH, font_size)
    for font_type, font_size in Font.SIZES.items()
}

screens: dict[GameState, BaseScreen] = {
    GameState.MAIN: MainScreen(fonts),
    GameState.GAME: GameScreen(fonts),
}
current_state = GameState.MAIN
pending_state: GameState | None = None
fade_started_at = 0
fade_mode: str | None = None


def start_fade(next_state):
    global pending_state, fade_started_at, fade_mode

    pending_state = next_state
    fade_started_at = pygame.time.get_ticks()
    fade_mode = "out"

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            screen_size = event.size
            screen = pygame.display.set_mode(screen_size, screen_flags)

        next_state = screens[current_state].handle_event(event)
        if next_state == GameState.EXIT:
            running = False
        elif next_state is not None and fade_mode is None:
            start_fade(next_state)

    screens[current_state].update()
    screens[current_state].draw(screen)

    if fade_mode is not None:
        elapsed = pygame.time.get_ticks() - fade_started_at
        progress = min(1, elapsed / Screen.FADE_DURATION_MS)
        alpha = int(255 * progress) if fade_mode == "out" else int(255 * (1 - progress))

        fade_surface = pygame.Surface(screen.get_size())
        fade_surface.fill(Color.BLACK.value)
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))

        if progress >= 1 and fade_mode == "out" and pending_state is not None:
            current_state = pending_state
            if current_state == GameState.GAME:
                screens[GameState.GAME].open_slot(screens[GameState.MAIN].selected_slot)
            elif current_state == GameState.MAIN:
                screens[GameState.MAIN].slots = get_save_slots()
            pending_state = None
            fade_started_at = pygame.time.get_ticks()
            fade_mode = "in"
        elif progress >= 1 and fade_mode == "in":
            fade_mode = None

    pygame.display.update()
    clock.tick(Screen.FPS)

pygame.quit()
