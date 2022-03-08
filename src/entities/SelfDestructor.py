import os
import pygame

from ..components.Components import HealthComponent, TransformComponent, RigidComponent
from ..render.renderer import Renderer
from ..settings import Settings

from math import sqrt

# SelfDestructor class
class SelfDestructor():
    
    _type = "SelfDestructor"
    _collider = 1 #CIRCLE

    collider_scale = 0.925
    scale = (0.8, 0.8)

    def __init__(self, position=[0.0,0.0], rotation=0.0, max_health=10, speed=130, damage=15, raycaster=None, stage=1):
        self.health = HealthComponent(self.on_death, max_health)
        
        self.transform = TransformComponent(position, rotation)
        self.rigidBody = RigidComponent(self.transform, speed+stage*5, on_touch=self.on_touch)

        self.min_target_range = 300
        self.damage = damage
        self.target = False

        self.size = (self.scale[0] * Renderer.image_cords[self._type][2], self.scale[1] * Renderer.image_cords[self._type][3])
        self.raycaster = raycaster

        self.destroyed = False


    def __str__(self):
        return f"SelfDestructor: {self.name}"


    def _update(self, dt):
        if self.can_see_target():
            self.rigidBody.rotate_towards_point(self.target.transform.position)
            self.rigidBody.move_towards_point(self.target.transform.position)

            self.rigidBody.update_position(dt)

        else:
            self.rigidBody.stand_still()


    def is_target_in_range(self):
        if self.target:
            dist_x = self.target.transform.position[0] - self.transform.position[0]
            dist_y = self.target.transform.position[1] - self.transform.position[1]

            return sqrt(dist_x ** 2 + dist_y ** 2) <= self.min_target_range
        
        return False


    def can_see_target(self):
        if self.target:
            return self.raycaster.check_if_path_clear(self.transform.position, self.target.transform.position)

        return False


    def set_target(self, target):
        if hasattr(target, "transform"):
            self.target = target


    def unset_target(self):
        self.target = False


    def on_death(self):
        pygame.event.post(pygame.event.Event(pygame.USEREVENT, {"user_type": "ENEMY_DIED"}))
        self.destroyed = True


    def on_touch(self, other):
        if other.transform is self.transform:
            return

        if other._type == "Player":
            self.on_death()

            sound = pygame.mixer.Sound(os.path.join("assets", "explosion.wav"))
            sound.set_volume(Settings.sound_volume/100)
            pygame.mixer.Sound.play(sound)

            if hasattr(other, "health"):
                other.health.take_damage(self.damage)