from enum import Enum

class ScreenState(Enum):
    MAIN_MENU = 1,
    PLAYING = 2,
    PAUSED = 3,
    PLAYER_DIED = 4,
    GIVE_POWERUP = 5,
    POWERUP1 = 6,
    POWERUP2 = 7,
    GAME_OVER = 8,