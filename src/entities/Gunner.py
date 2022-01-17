import pygame

from ..components.Components import HealthComponent, TransformComponent, RigidComponent, GunComponent
from ..render.renderer import Renderer

from math import sqrt

# Gunner class
class Gunner():
    
    _type = "Gunner"
    _collider = 1 #CIRCLE

    collider_scale = 0.925
    scale = (1.1, 1.1)

    def __init__(self, position=[0.0,0.0], rotation=0.0, max_health=100, speed=30, raycaster=None):
        self.health = HealthComponent(self.on_death, max_health)
        
        self.transform = TransformComponent(position, rotation)
        self.rigidBody = RigidComponent(self.transform, speed)

        self.gun = GunComponent(["Player"], self.transform, fire_rate=1.5, semi_auto=False, projectile_type="RED")

        self.min_target_range = 500
        self.target = False
        
        self.size = (self.scale[0] * Renderer.image_cords[self._type][2], self.scale[1] * Renderer.image_cords[self._type][3])
        self.raycaster = raycaster

        self.destroyed = False


    def __str__(self):
        return f"Gunner: {self.name}"


    def _update(self, dt):
        if self.can_see_target():
            self.rigidBody.rotate_towards_point(self.target.transform.position)
            self.rigidBody.move_towards_point(self.target.transform.position)

            self.rigidBody.update_position(dt)

            self.gun.shoot(self.target.transform.position)
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