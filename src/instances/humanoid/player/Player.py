import pygame
import pygame.mouse as mouse

from math import atan2, pi
from ..Humanoid import Humanoid

# player class
class Player(Humanoid):
    
    _type = "Player"

    def __init__(self, name, position=[0.0,0.0], rotation=0.0, max_health=100):
        super().__init__(name, position, rotation)
        self.speed = 120


    def __str__(self):
        return f"Player: {self.name}"


    def _update(self, dt):
        keystate = pygame.key.get_pressed()
        mouse_pos = mouse.get_pos()

        move_vec = [keystate[pygame.K_RIGHT] - keystate[pygame.K_LEFT] + self.position[0], keystate[pygame.K_DOWN] - keystate[pygame.K_UP] + self.position[1]]

        self.move_towards_point(move_vec)
        self.rotate_towards_point(mouse_pos)
        
        self.position = [self.position[0] + self.velocity[0]*self.speed*dt, self.position[1] + self.velocity[1]*self.speed*dt]
