import pygame.mouse as mouse

from math import atan2, pi
from ..Humanoid import Humanoid

# zombie class
class Zombie(Humanoid):
    
    _type = "Zombie"

    def __init__(self, name, position=[0.0,0.0], rotation=0.0, max_health=100):
        super().__init__(name, position, rotation)


    def __str__(self):
        return f"Zombie: {self.name}"


    def _update(self, dt):
        mouse_pos = mouse.get_pos()

        # update rotation
        self.rotation = 360 - atan2(mouse_pos[1] - self.position[1], mouse_pos[0] - self.position[0]) *180/pi
