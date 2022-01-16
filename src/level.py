# instances
from .entities.Player import Player
from .entities.Zombie import Zombie
from .entities.Gunner import Gunner
from .entities.SelfDestructor import SelfDestructor
from .entities.Tile import Tile

from .physics.raycaster import Raycaster


# defaults
default_level = "test"
premade_levels = {
    "test": {
        "player": {"position": [300.0, 550.0], "rotation":-110.0},
        "zombies": [[100.0, 100.0], [200.0, 100.0],],
        "gunners": [[140.0, 150.0], [240.0, 140.0],],
        "self_destructors": [[150.0, 160.0], [260.0, 160.0],],

        "map_tiles": {
            "GrassTile": [[300.0, 300.0]],
        },

        "background": "BackgroundYellow",
    },
}


# level generation data
enemy_types = {
    "Zombie": {"min_stage":0, "class": Zombie, "rarity": 10},
    "Gunner": {"min_stage":0, "class": Gunner, "rarity": 5},
    "SelfDestructor": {"min_stage":0, "class": SelfDestructor, "rarity": 5},
}

background_types = {
    "BackgroundYellow": {"rarity":10},
    "BackgroundGreen": {"rarity":10},
    "BackgroundRed": {"rarity":10},
    "BackgroundBlue": {"rarity":10},
}


class Level:
    
    def __init__(self, level):
        if not level in premade_levels:
            self.data = premade_levels[default_level]
        else:
            self.data = premade_levels[level]

    def load_scene(self):
        self.scene = {
            "BACKGROUND": set(),
            "MAP": set(),
            "TO_DRAW": set(),
            "PLAYER": set(),
            "ENEMIES": set(),
            "COLLIDABLE": set(),
            "WITH_GUN": set(),
        }


        # make map
        for tile_type, positions in self.data["map_tiles"].items():
            for pos in positions:
                new_tile = Tile(pos, 0.0, _type=tile_type)
                self.scene["MAP"].add(new_tile)
                self.scene["COLLIDABLE"].add(new_tile)

        # create a raycaster that will work for the current map
        self.raycaster = Raycaster(self.scene["MAP"])


        player = Player(self.data["player"]["position"], self.data["player"]["rotation"])
        self.scene["PLAYER"].add(player)
        self.scene["TO_DRAW"].add(player)
        self.scene["COLLIDABLE"].add(player)
        self.scene["WITH_GUN"].add(player)

        self.scene["BACKGROUND"].add(self.data["background"])

        for pos in self.data["zombies"]:
            new_zombie = Zombie(pos, 0.0, raycaster=self.raycaster)
            new_zombie.set_target(player)
            self.scene["TO_DRAW"].add(new_zombie)
            self.scene["ENEMIES"].add(new_zombie)
            self.scene["COLLIDABLE"].add(new_zombie)

        for pos in self.data["gunners"]:
            new_gunner = Gunner(pos, 0.0, raycaster=self.raycaster)
            new_gunner.set_target(player)
            self.scene["TO_DRAW"].add(new_gunner)
            self.scene["ENEMIES"].add(new_gunner)
            self.scene["COLLIDABLE"].add(new_gunner)
            self.scene["WITH_GUN"].add(new_gunner)

        for pos in self.data["gunners"]:
            new_self_destructor = SelfDestructor(pos, 0.0, raycaster=self.raycaster)
            new_self_destructor.set_target(player)
            self.scene["TO_DRAW"].add(new_self_destructor)
            self.scene["ENEMIES"].add(new_self_destructor)
            self.scene["COLLIDABLE"].add(new_self_destructor)


    def add_projectile(self, projectile):
        self.scene["TO_DRAW"].add(projectile)
        self.scene["COLLIDABLE"].add(projectile)


    def generate_level(self, stage=1):
        pass
