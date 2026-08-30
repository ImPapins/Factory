from enum import Enum, auto


class ScreenState(Enum):
    MAIN = auto()
    GAME = auto()
    EXIT = auto()

class TransitionParam(Enum):
    SAVE_SLOT = auto()   # 선택된 SaveSlot 객체

class Color(Enum):
    BACKGROUND = (24, 28, 34)
    GAME_BACKGROUND = (30, 160, 90)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    PANEL = (48, 56, 66)
    PANEL_HOVER = (68, 78, 92)
    ACCENT = (255, 184, 77)
    DANGER = (210, 80, 80)
    DANGER_HOVER = (235, 100, 100)


class FontType(Enum):
    TITLE = auto()
    BODY = auto()
    SMALL = auto()


class Screen:
    TITLE = "Automation Factory"
    WIDTH = 800
    HEIGHT = 600
    FPS = 60
    RESIZABLE = True
    FADE_DURATION_MS = 1000


class Font:
    PATH = None
    SIZES = {
        FontType.TITLE: 56,
        FontType.BODY: 34,
        FontType.SMALL: 20,
    }
