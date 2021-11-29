from ..components.Components import HealthComponent, TransformComponent, RigidComponent

from math import sqrt

# zombie class
class Zombie():
    
    _type = "Zombie"

    def __init__(self, position=[0.0,0.0], rotation=0.0, max_health=100, speed=50):
        self.health = HealthComponent(self.on_death, max_health)
        
        self.transform = TransformComponent(position, rotation)
        self.rigidBody = RigidComponent(self.transform, speed)

        self.min_target_range = 200
        self.target = False

        self.destroyed = False


    def __str__(self):
        return f"Zombie: {self.name}"


    def _update(self, dt):
        if self.is_target_in_range():
            self.rigidBody.rotate_towards_point(self.target.transform.position)
            self.rigidBody.move_towards_point(self.target.transform.position)

            self.rigidBody.update_position(dt)

        else:
            self.rigidBody.stand_still()


    def is_target_in_range(self):
        if self.target:
            dist_x = self.target.transform.position[0] - self.transform.position[0]
            dist_y = self.target.transform.position[1] - self.transform.position[1]

            return sqrt(dist_x ** 2 + dist_y ** 2) <= self.min_target_range
        
        return False


    def set_target(self, target):
        if hasattr(target, "transform"):
            self.target = target


    def unset_target(self):
        self.target = False


    def on_death(self):
        print("dead")
        self.destroyed = True