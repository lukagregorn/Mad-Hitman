import os
from pygame import mixer

from components.Components import TransformComponent, RigidComponent
from renderer import Renderer
from settings import Settings


PROJECTILE_TYPES = {
    "YELLOW": {
        "speed": 300,
        "damage": 10,
        "scale": (0.7, 0.7),
        "_type": "ProjectileYellow",
        "sound": "shoot1.wav",
    },

    "RED": {
        "speed": 250,
        "damage": 5,
        "scale": (1.2, 1.2),
        "_type": "ProjectileRed",
        "sound": "shoot2.wav",
    },

    "BOSS": {
        "speed": 400,
        "damage": 5,
        "scale": (1.4, 1.4),
        "_type": "ProjectileBoss",
        "sound": "shoot2.wav",
    },

    "BOSS_BIG": {
        "speed": 400,
        "damage": 5,
        "scale": (2.3, 2.3),
        "_type": "ProjectileBoss",
        "sound": "shoot2.wav",
    },
}

# projecitle class
class Projectile():
    
    _type = "Projectile"
    _collider = 1 #CIRCLE

    collider_scale = 1.0

    def __init__(self, position=[0.0,0.0], target=[0.0,0.0], only_hit_types=[], parent_transform=None, projectile_type="YELLOW", speed_multi=1.0, damage_multi=1.0):
        self.transform = TransformComponent(position)
        self.rigidBody = RigidComponent(self.transform, PROJECTILE_TYPES[projectile_type]["speed"]*speed_multi, on_touch=self.on_touch)

        self.rigidBody.rotate_towards_point(target)
        self.rigidBody.move_towards_point(target)

        self.damage = PROJECTILE_TYPES[projectile_type]["damage"] * damage_multi
        self.only_hit_types = only_hit_types

        self.scale = PROJECTILE_TYPES[projectile_type]["scale"]
        self._type = PROJECTILE_TYPES[projectile_type]["_type"]

        self.size = (self.scale[0] * Renderer.image_cords[self._type][2], self.scale[1] * Renderer.image_cords[self._type][3])

        self.parent_transform = parent_transform
        self.destroyed = False

        # play sound
        sound = mixer.Sound(os.path.join("assets", PROJECTILE_TYPES[projectile_type]["sound"]))
        sound.set_volume(Settings.sound_volume/100)
        mixer.Sound.play(sound)

    def _update(self, dt):
        self.rigidBody.update_position(dt)

        # check out of screen
        pos = self.rigidBody.transform.position
        if (pos[1] > Settings.screen_height or pos[1] < 0 or pos[0] > Settings.screen_width or pos[0] < 0):
            self.destroyed = True


    def on_touch(self, other):
        if other.transform is self.parent_transform:
            return

        if not other._type in self.only_hit_types:
            return

        if not other._type == self._type:
            self.destroyed = True

            if hasattr(other, "health"):
                other.health.take_damage(self.damage)

