from ..Humanoid import Humanoid

from math import sqrt

# zombie class
class Zombie(Humanoid):
    
    _type = "Zombie"

    def __init__(self, name, position=[0.0,0.0], rotation=0.0, max_health=100):
        super().__init__(name, position, rotation)
        
        self.min_target_range = 200
        self.target = False


    def __str__(self):
        return f"Zombie: {self.name}"


    def _update(self, dt):
        if self.is_target_in_range():
            self.rotate_towards_point(self.target.position)
            self.move_towards_point(self.target.position)

            self.position = [self.position[0] + self.velocity[0]*self.speed*dt, self.position[1] + self.velocity[1]*self.speed*dt]

        else:
            self.stand_still()


    def is_target_in_range(self):
        if self.target:
            dist_x = self.target.position[0] - self.position[0]
            dist_y = self.target.position[1] - self.position[1]

            return sqrt(dist_x ** 2 + dist_y ** 2) <= self.min_target_range
        
        return False

    def set_target(self, target):
        self.target = target

    def unset_target(self):
        self.target = False