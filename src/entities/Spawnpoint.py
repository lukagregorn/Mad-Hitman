import imp
from random import randrange

from ..components.Components import TransformComponent
from ..render.renderer import Renderer

class Spawnpoint():
    
    _type = "Spawnpoint"
    scale = (1.0, 1.0)

    def __init__(self, position=[0.0,0.0]):
        
        self.transform = TransformComponent(position, randrange(-180, 180))
        self.size = (self.scale[0] * Renderer.image_cords[self._type][2], self.scale[1] * Renderer.image_cords[self._type][3])

        self.destroyed = False

    def __str__(self):
        return f"Spawnpoint: {self._type}"


    def _update(self, dt):
        pass
