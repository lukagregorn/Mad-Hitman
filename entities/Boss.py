import pygame

from components.Components import HealthComponent, TransformComponent, RigidComponent, GunComponent
from renderer import Renderer

from random import choice

# Boss class
class Boss():
    
    _type = "Boss"
    _collider = 1 #CIRCLE

    collider_scale = 0.925
    scale = (1.1, 1.1)

    cooldown_time = 4
    cooldown_wait = 2

    move_set = [
        {
            "recoil": 420,
            "fire_rate": 0.1,
            "damage_multi": 0.8,
            "speed_multi": 0.65,
            "projectile_type": "BOSS",

            "duration": 6,
        },

        {
            "recoil": 10,
            "fire_rate": 0.6,
            "damage_multi": 1.1,
            "speed_multi": 2.2,
            "projectile_type": "BOSS_BIG",

            "duration": 2.5,
        },

        {
            "recoil": 40,
            "fire_rate": 0.05,
            "damage_multi": 1,
            "speed_multi": 1.1,
            "projectile_type": "BOSS",

            "duration": 4,
        },
    ]

    def __init__(self, position=[0.0,0.0], rotation=0.0, max_health=300, speed=30, raycaster=None, stage=1):
        self.health = HealthComponent(self.on_death, max_health+50*stage)
        
        self.transform = TransformComponent(position, rotation)
        self.rigidBody = RigidComponent(self.transform, speed)

        self.gun = GunComponent(["Player"], self.transform, semi_auto=False)
        self.set_gun_config(choice(self.move_set))

        self.min_target_range = 500
        self.target = False
        
        self.size = (self.scale[0] * Renderer.image_cords[self._type][2], self.scale[1] * Renderer.image_cords[self._type][3])
        self.raycaster = raycaster

        self.cooldown = 0
        self.wait_time = 0
        self.destroyed = False


    def __str__(self):
        return f"Boss: {self.name}"


    def _update(self, dt):
        if self.cooldown >= self.cooldown_time:
            self.wait_time += dt
            if self.wait_time >= self.cooldown_wait:
                self.set_gun_config(choice(self.move_set))
                self.cooldown = 0
                self.wait_time = 0
        else:
            self.cooldown += dt
            self.rigidBody.rotate_towards_point(self.target.transform.position)
            self.gun.shoot(self.target.transform.position)


    def set_gun_config(self, config):
        self.gun.recoil = config["recoil"]
        self.gun.fire_rate = config["fire_rate"]
        self.gun.damage_multi = config["damage_multi"]
        self.gun.speed_multi = config["speed_multi"]
        self.gun.projectile_type = config["projectile_type"]

        self.cooldown_time = config["duration"]


    def set_target(self, target):
        if hasattr(target, "transform"):
            self.target = target


    def unset_target(self):
        self.target = False


    def on_death(self):
        pygame.event.post(pygame.event.Event(pygame.USEREVENT, {"user_type": "ENEMY_DIED"}))
        self.destroyed = True