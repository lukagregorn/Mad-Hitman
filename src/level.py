# instances
from .entities.Player import Player
from .entities.Zombie import Zombie


# defaults
default_level = "test"
premade_levels = {
    "test": {
        "player": {"position": [300.0, 400.0], "rotation":-110.0},
        "zombies": [[100.0, 100.0], [200.0, 100.0], [300.0, 100.0]]
    },
}


class Level:
    
    def __init__(self, level):
        if not level in premade_levels:
            self.data = premade_levels[default_level]
        else:
            self.data = premade_levels[level]

    def load_scene(self):
        self.scene = {
            "TO_DRAW": set(),
            "WITH_GUN": set(),
            "COLLIDABLE": set(),
        }

        player = Player(self.data["player"]["position"], self.data["player"]["rotation"])
        print(player.size)
        self.scene["TO_DRAW"].add(player)
        self.scene["WITH_GUN"].add(player)
        self.scene["COLLIDABLE"].add(player)

        for pos in self.data["zombies"]:
            new_zombie = Zombie(pos, 0.0)
            new_zombie.set_target(player)
            self.scene["TO_DRAW"].add(new_zombie)
            self.scene["COLLIDABLE"].add(new_zombie)

    
    def add_projectile(self, projectile):
        self.scene["TO_DRAW"].add(projectile)
        self.scene["COLLIDABLE"].add(projectile)