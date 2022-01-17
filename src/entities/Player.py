from typing import Sized
import pygame
import pygame.mouse as mouse

from ..components.Components import HealthComponent, TransformComponent, RigidComponent, GunComponent
from ..render.renderer import Renderer


# player class
class Player():
    
    _type = "Player"
    _collider = 1 #CIRCLE

    collider_scale = 0.925
    scale = (1.1, 1.1)

    def __init__(self, position=[0.0,0.0], rotation=0.0, max_health=100, speed=120, raycaster=None):

        self.health = HealthComponent(self.on_death, max_health, self.on_health_changed)
        
        self.transform = TransformComponent(position, rotation)
        self.rigidBody = RigidComponent(self.transform, speed, clamp_to_screen=True)
        
        self.gun = GunComponent(["Gunner", "Zombie", "SelfDestructor"], self.transform, fire_rate=0.25, semi_auto=False, projectile_type="YELLOW", recoil=15)

        self.last_rot_vec = [0.0, 0.0]

        self.size = (self.scale[0] * Renderer.image_cords[self._type][2], self.scale[1] * Renderer.image_cords[self._type][3])
        self.raycaster = raycaster

        self.destroyed = False
        self.on_health_changed(self.health.health)


    def __str__(self):
        return f"Player: {self.name}"


    def _update(self, dt):

        keystate = pygame.key.get_pressed()
        #mouse_pos = mouse.get_pos()
 
        move_vec = [keystate[pygame.K_RIGHT] - keystate[pygame.K_LEFT] + self.transform.position[0], keystate[pygame.K_DOWN] - keystate[pygame.K_UP] + self.transform.position[1]]
        self.rigidBody.move_towards_point(move_vec)

        negate_rot = False
        if abs(self.rigidBody.velocity[0]) <= 0.01 and abs(self.rigidBody.velocity[1]) <= 0.01:
    
            target = self.raycaster.find_visible_enemy(self.transform.position)
            if target:
                self.gun.shoot(target.transform.position)
                self.last_rot_vec = target.transform.position

            else:
                negate_rot = True

        else:
            self.last_rot_vec = move_vec
        
        self.rigidBody.rotate_towards_point(self.last_rot_vec, negate=negate_rot)
        self.rigidBody.update_position(dt)                

        #if mouse.get_pressed()[0]:
        #    self.gun.shoot(mouse_pos)
        #else:
        #    self.gun.release_trigger()

    def on_death(self):
        self.destroyed = True
        pygame.event.post(pygame.event.Event(pygame.USEREVENT, {"user_type": "PLAYER_DIED"}))

    def on_health_changed(self, new_health):
        pygame.event.post(pygame.event.Event(pygame.USEREVENT, {"user_type": "HEALTH_CHANGED", "player_health": new_health}))

    def set_raycaster(self, raycaster=None):
        self.raycaster = raycaster

    def reset_position(self, position, rotation):
        self.last_rot_vec = [0,0]
        self.transform.position = position
        self.transform.rotation = rotation