import pygame
from math import atan2, pi, sqrt
from pygame.time import wait


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


class HealthComponent:
    def __init__(self, on_death, max_health):
        self.max_health = max_health
        self.health = max_health

        # callback function on death
        self.on_death = on_death


    def take_damage(self, damage):
        self.health -= damage

        if self.health <= 0:
            self.on_death()


class TransformComponent:
    def __init__(self, position=[0.0,0.0], rotation=0.0):
        self.position = position
        self.rotation = rotation


class RigidComponent:
    def __init__(self, transform, speed=40, canCollide=True, on_touch=None, static=False):

        if not transform:
            return None
        
        self.transform = transform

        # initial values
        self.velocity = [0, 0]
        self.speed = speed

        self.on_touch = on_touch
        self.canCollide = canCollide
        self.static = static


    def rotate_towards_point(self, target_point):
        self.transform.rotation = 360 - atan2(target_point[1] - self.transform.position[1], target_point[0] - self.transform.position[0]) *180/pi


    def move_towards_point(self, target_point):
        dir_x = target_point[0] - self.transform.position[0]
        dir_y = target_point[1] - self.transform.position[1]

        dir_len = sqrt(dir_x ** 2 + dir_y ** 2)
        if (dir_len > 0):
            self.velocity = [dir_x/dir_len, dir_y/dir_len]
        else:
            self.stand_still()


    def stand_still(self):
        self.velocity = [0, 0]


    def update_position(self, dt):
        self.transform.position = [self.transform.position[0] + self.velocity[0]*self.speed*dt, self.transform.position[1] + self.velocity[1]*self.speed*dt]


class GunComponent:
    def __init__(self, transform, fire_rate=0.5, semi_auto=True):

        if not transform:
            return None
        
        self.transform = transform

        # initial values
    
        self.semi_auto = semi_auto
        self.is_ready = True # used for semi auto

        self.can_shoot = 0
        self.fire_rate = fire_rate

        # projectiles to generate
        self._projectiles_to_spawn = []

    def _update_gun(self, dt):
        if (self.can_shoot > 0):
            self.can_shoot -= dt

        return self._projectiles_to_spawn


    def release_trigger(self):
        self.is_ready = True


    def shoot(self, target=[0.0, 0.0]):
        if self.can_shoot > 0 or not self.is_ready:
            return
        
        self.can_shoot = self.fire_rate
        if (self.semi_auto):
            self.is_ready = False

        dir_x = target[0] - self.transform.position[0]
        dir_y = target[1] - self.transform.position[1]

        dir_len = sqrt(dir_x ** 2 + dir_y ** 2)
        scale = 30
        dir = [dir_x/dir_len * scale, dir_y/dir_len * scale]

        data = {
            "target": target,
            "position": [self.transform.position[0] + dir[0], self.transform.position[1] + dir[1]],
            "parent_transform": self.transform,
        }

        self._projectiles_to_spawn.append(data)



            

        




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