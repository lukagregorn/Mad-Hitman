import os
from pygame import mixer

from ..components.Components import TransformComponent, RigidComponent
from ..render.renderer import Renderer

from math import sqrt

# SelfDestructor class
class Tile():
    
    _type = "Box"
    _collider = 0 #RECT
    
    _destroy_on_touch = {"ProjectileYellow", "ProjectileRed"}

    collider_scale = 1.0
    scale = (1.0, 1.0)

    def __init__(self, position=[0.0,0.0], rotation=0.0, can_collide=True, _type="Box"):
        
        self._type = _type

        self.transform = TransformComponent(position, rotation)
        self.rigidBody = RigidComponent(self.transform, static=True, on_touch=self.on_touch, canCollide=can_collide)

        self.size = (self.scale[0] * Renderer.image_cords[self._type][2], self.scale[1] * Renderer.image_cords[self._type][3])

        self.destroyed = False

    def __str__(self):
        return f"Tile: {self._name}"


    def _update(self, dt):
        pass


    def on_touch(self, other):
        if other.transform is self.transform:
            return

        if other._type in self._destroy_on_touch:
            other.destroyed = True
        else:
            other.transform.position[0] -= other.rigidBody.last_position_change[0]
            other.transform.position[1] -= other.rigidBody.last_position_change[1]