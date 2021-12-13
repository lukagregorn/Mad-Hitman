from ..components.Components import TransformComponent, RigidComponent
from ..render.renderer import Renderer


PROJECTILE_TYPES = {
    "YELLOW": {
        "speed": 300,
        "damage": 10,
        "scale": (0.7, 0.7),
        "_type": "ProjectileYellow",
    },

    "RED": {
        "speed": 250,
        "damage": 5,
        "scale": (1.2, 1.2),
        "_type": "ProjectileRed",
    },
}

# projecitle class
class Projectile():
    
    _type = "Projectile"

    def __init__(self, position=[0.0,0.0], target=[0.0,0.0], only_hit_types=[], parent_transform=None, projectile_type="YELLOW"):
        self.transform = TransformComponent(position)
        self.rigidBody = RigidComponent(self.transform, PROJECTILE_TYPES[projectile_type]["speed"], on_touch=self.on_touch)

        self.rigidBody.rotate_towards_point(target)
        self.rigidBody.move_towards_point(target)

        self.damage = PROJECTILE_TYPES[projectile_type]["damage"]
        self.only_hit_types = only_hit_types

        self.scale = PROJECTILE_TYPES[projectile_type]["scale"]
        self._type = PROJECTILE_TYPES[projectile_type]["_type"]

        self.size = (self.scale[0] * Renderer.image_cords[self._type][2], self.scale[1] * Renderer.image_cords[self._type][3])

        self.parent_transform = parent_transform
        self.destroyed = False

    def _update(self, dt):
        self.rigidBody.update_position(dt)


    def on_touch(self, other):
        if other.transform is self.parent_transform:
            return

        if not other._type in self.only_hit_types:
            return

        if not other._type == self._type:
            self.destroyed = True

            if hasattr(other, "health"):
                other.health.take_damage(self.damage)

