# instances
from .entities.Player import Player
from .entities.Zombie import Zombie
from .entities.Gunner import Gunner
from .entities.SelfDestructor import SelfDestructor


# defaults
default_level = "test"
premade_levels = {
    "test": {
        "player": {"position": [300.0, 500.0], "rotation":-110.0},
        "zombies": [[100.0, 100.0], [200.0, 100.0],],
        "gunners": [[140.0, 150.0], [240.0, 140.0],],
        "self_destructors": [[150.0, 160.0], [260.0, 160.0],],
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
            "PLAYER": set(),
            "ENEMIES": set(),
            "COLLIDABLE": set(),
            "WITH_GUN": set(),
        }

        player = Player(self.data["player"]["position"], self.data["player"]["rotation"])
        print(player.size)
        self.scene["PLAYER"].add(player)
        self.scene["TO_DRAW"].add(player)
        self.scene["COLLIDABLE"].add(player)
        self.scene["WITH_GUN"].add(player)

        for pos in self.data["zombies"]:
            new_zombie = Zombie(pos, 0.0)
            new_zombie.set_target(player)
            self.scene["TO_DRAW"].add(new_zombie)
            self.scene["ENEMIES"].add(new_zombie)
            self.scene["COLLIDABLE"].add(new_zombie)

        for pos in self.data["gunners"]:
            new_gunner = Gunner(pos, 0.0)
            new_gunner.set_target(player)
            self.scene["TO_DRAW"].add(new_gunner)
            self.scene["ENEMIES"].add(new_gunner)
            self.scene["COLLIDABLE"].add(new_gunner)
            self.scene["WITH_GUN"].add(new_gunner)

        for pos in self.data["gunners"]:
            new_self_destructor = SelfDestructor(pos, 0.0)
            new_self_destructor.set_target(player)
            self.scene["TO_DRAW"].add(new_self_destructor)
            self.scene["ENEMIES"].add(new_self_destructor)
            self.scene["COLLIDABLE"].add(new_self_destructor)

    
    def add_projectile(self, projectile):
        self.scene["TO_DRAW"].add(projectile)
        self.scene["COLLIDABLE"].add(projectile)