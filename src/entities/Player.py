import pygame
import pygame.mouse as mouse

from ..components.Components import HealthComponent, TransformComponent, RigidComponent, GunComponent

# player class
class Player():
    
    _type = "Player"

    def __init__(self, position=[0.0,0.0], rotation=0.0, max_health=100, speed=120):

        self.health = HealthComponent(self.on_death, max_health)
        
        self.transform = TransformComponent(position, rotation)
        self.rigidBody = RigidComponent(self.transform, speed)
        
        self.gun = GunComponent(self.transform, fire_rate=0.1, semi_auto=False)

        self.destroyed = False


    def __str__(self):
        return f"Player: {self.name}"


    def _update(self, dt):

        keystate = pygame.key.get_pressed()
        mouse_pos = mouse.get_pos()
 
        move_vec = [keystate[pygame.K_RIGHT] - keystate[pygame.K_LEFT] + self.transform.position[0], keystate[pygame.K_DOWN] - keystate[pygame.K_UP] + self.transform.position[1]]

        self.rigidBody.move_towards_point(move_vec)
        self.rigidBody.rotate_towards_point(mouse_pos)

        self.rigidBody.update_position(dt)

        #if (self.rigidBody.velocity[0] == self.rigidBody.velocity[1] == 0):
        #    self.gun.shoot()
        if mouse.get_pressed()[0]:
            self.gun.shoot(mouse_pos)
        else:
            self.gun.release_trigger()

    def on_death(self):
        self.destroyed = True