import pygame, os
from math import atan2, pi, sqrt
from random import uniform
from pygame.time import wait

from ..settings import Settings


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
    def __init__(self, on_death, max_health, on_health_changed=None):
        self.max_health = max_health
        self.health = max_health

        # callback function on death
        self.on_death = on_death
        self.on_health_changed = on_health_changed


    def take_damage(self, damage):
        self.health -= damage

        if self.on_health_changed:
            self.on_health_changed(self.health)

        sound = pygame.mixer.Sound(os.path.join("assets", "hit.wav"))
        pygame.mixer.Sound.play(sound)

        if self.health <= 0 and self.on_death:
            self.on_death()


class TransformComponent:
    def __init__(self, position=[0.0,0.0], rotation=0.0):
        self.position = position
        self.rotation = rotation


class RigidComponent:
    def __init__(self, transform, speed=40, canCollide=True, on_touch=None, static=False, clamp_to_screen=False):

        if not transform:
            return None
        
        self.transform = transform

        # initial values
        self.velocity = [0, 0]
        self.speed = speed
        self.last_position_change = [0,0]

        self.on_touch = on_touch
        self.canCollide = canCollide
        self.static = static
        self.clamp_to_screen = clamp_to_screen


    def rotate_towards_point(self, target_point, negate=False):
        new_rot = 360 - atan2(target_point[1] - self.transform.position[1], target_point[0] - self.transform.position[0]) *180/pi
        if negate:
            self.transform.rotation = 180 + new_rot
        else:
            self.transform.rotation = new_rot


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
        self.last_position_change = [self.velocity[0]*self.speed*dt, self.velocity[1]*self.speed*dt]
        self.transform.position = [self.transform.position[0] + self.last_position_change[0], self.transform.position[1] + self.last_position_change[1]]
        if (self.clamp_to_screen):

            self.transform.position[0] = min(max(0, self.transform.position[0]), Settings.screen_width)
            self.transform.position[1] = min(max(0, self.transform.position[1]), Settings.screen_height)

class GunComponent:
    def __init__(self, only_hit_types, transform, fire_rate=0.5, semi_auto=True, projectile_type="YELLOW", recoil=50):

        if not transform:
            return None
        
        self.transform = transform

        # filter
        self.only_hit_types = only_hit_types

        # initial values
        self.projectile_type = projectile_type
        self.semi_auto = semi_auto
        self.is_ready = True # used for semi auto

        self.can_shoot = 0
        self.fire_rate = fire_rate
        self.recoil = recoil

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
        target = [target[0] + uniform(-1.0, 1.0)*self.recoil, target[1] + uniform(-1.0, 1.0)*self.recoil]

        data = {
            "target": target,
            "position": [self.transform.position[0] + dir[0], self.transform.position[1] + dir[1]],
            "parent_transform": self.transform,
            "only_hit_types": self.only_hit_types,
            "projectile_type": self.projectile_type,
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