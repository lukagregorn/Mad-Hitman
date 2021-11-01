from ..Instance import Instance

# player class
class Humanoid(Instance):
    
    _type = "Humanoid"

    def __init__(self, name="Humanoid", position=[0.0,0.0], rotation=0.0, max_health=100):
        super().__init__(name, position, rotation)

        # initial velocity
        self.velocity = [0, 0]
        self.speed = 10

        self.max_health = max_health
        self.health = max_health
