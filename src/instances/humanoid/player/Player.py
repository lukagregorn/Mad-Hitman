import pygame.mouse as mouse

from math import atan2, pi
from instances.humanoid.Humanoid import Humanoid
from ..Humanoid import Humanoid

# player class
class Player(Humanoid):
    
    _type = "Player"

    def __init__(self, name, position=[0.0,0.0], rotation=0.0, max_health=100):
        super().__init__(name, position, rotation)


    def __str__(self):
        return f"Player: {self.name}"

    def _update(self, dt):
        mouse_pos = mouse.get_pos()

        # update rotation
        self.rotation = 360 - atan2(mouse_pos[1] - self.position[1], mouse_pos[0] - self.position[0]) *180/pi
