from ..components.Components import TransformComponent, RigidComponent

from math import sqrt

# zombie class
class Projectile():
    
    _type = "Projectile"

    def __init__(self, position=[0.0,0.0], target=[0.0,0.0], speed=300, damage=10, parent_transform=None):
        self.transform = TransformComponent(position)
        self.rigidBody = RigidComponent(self.transform, speed, on_touch=self.on_touch)

        self.rigidBody.rotate_towards_point(target)
        self.rigidBody.move_towards_point(target)

        self.damage = damage

        self.parent_transform = parent_transform
        self.destroyed = False

    def _update(self, dt):
        self.rigidBody.update_position(dt)


    def on_touch(self, other):
        if other.transform is self.parent_transform:
            return

        if not other._type == self._type:
            self.destroyed = True

            if hasattr(other, "health"):
                other.health.take_damage(self.damage)

