from ..Instance import Instance

from math import atan2, pi, sqrt

# player class
class Humanoid(Instance):
    
    _type = "Humanoid"

    def __init__(self, name="Humanoid", position=[0.0,0.0], rotation=0.0, max_health=100):
        super().__init__(name, position, rotation)

        # initial velocity
        self.velocity = [0, 0]
        self.speed = 40

        self.max_health = max_health
        self.health = max_health


    def rotate_towards_point(self, target_point):
        self.rotation = 360 - atan2(target_point[1] - self.position[1], target_point[0] - self.position[0]) *180/pi


    def move_towards_point(self, target_point):
        dir_x = target_point[0] - self.position[0]
        dir_y = target_point[1] - self.position[1]

        dir_len = sqrt(dir_x ** 2 + dir_y ** 2)
        if (dir_len > 0):
            self.velocity = [dir_x/dir_len, dir_y/dir_len]
        else:
            self.stand_still()


    def stand_still(self):
        self.velocity = [0, 0]