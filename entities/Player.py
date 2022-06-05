from matplotlib.colors import PowerNorm
import pygame
import pygame.mouse as mouse

from components.Components import HealthComponent, TransformComponent, RigidComponent, GunComponent
from renderer import Renderer


# player class
class Player():
    
    _type = "Player"
    _collider = 1 #CIRCLE

    collider_scale = 0.925
    scale = (1.1, 1.1)

    def __init__(self, position=[0.0,0.0], rotation=0.0, max_health=50, speed=120, raycaster=None):

        self.health = HealthComponent(self.on_death, max_health, self.on_health_changed)
        
        self.transform = TransformComponent(position, rotation)
        self.rigidBody = RigidComponent(self.transform, speed, clamp_to_screen=True)
        
        self.gun = GunComponent(["Gunner", "Zombie", "SelfDestructor", "Boss"], self.transform, fire_rate=0.75, semi_auto=False, projectile_type="YELLOW", recoil=45)

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

    def apply_powerup(self, powerup):
        powerup_key = powerup[0]
        powerup_value = powerup[1]

        if powerup_key == "SPEED":
            self.rigidBody.speed *= powerup_value

        if powerup_key == "RECOIL":
            self.gun.recoil *= powerup_value
        
        if powerup_key == "HEALTH":
            self.health.max_health *= powerup_value

        if powerup_key == "FIRE RATE":
            self.gun.fire_rate *= powerup_value

        if powerup_key == "DAMAGE":
            self.gun.damage_multi *= powerup_value
        
        if powerup_key == "BULLET SPEED":
            self.gun.speed_multi *= powerup_value


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

    def respawn(self):
        self.rigidBody.speed = 120
        self.health.max_health = 50
        self.gun.fire_rate = 0.75
        self.gun.recoil = 45
        self.gun.damage_multi = 1
        self.gun.speed_multi = 1

        self.health.health = self.health.max_health
        self.health.on_health_changed(self.health.health)
        self.destroyed = False