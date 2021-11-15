import pygame


class SpriteComponent:
    def __init__(self, surface, initial_x, initial_y):
        self.surface = surface
        self.rect = self.surface.get_rect()
        self.rect.move_ip(initial_x, initial_y)


class AnimationComponent:
    def __init__(self, surfaces, interval_length):
        self.surfaces = surfaces
        self.interval_len = interval_length
        self.ani_cycle_count = 0


class RigidComponent:
    def __init__(self, x_velocity, y_velocity):
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity

"""
class TextComponent:
    def __init__(self, text, size, color):
        self.text = text
        self.size = size
        self.color = pygame.color.Color(color)
        self.font = pygame.font.Font(None, self.size)

        
class AudioComponent:
    def __init__(self, sound: pygame.mixer.Sound) -> None:
        self.sound = sound


class LifeTimeComponent:
    def __init__(self, life_time: int) -> None:
        self.life_time = life_time
"""