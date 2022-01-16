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
        "player": [300.0, 550.0],
        "zombies": [[100.0, 100.0], [200.0, 100.0],],
        "gunners": [[140.0, 150.0], [240.0, 140.0],],
        "self_destructors": [[150.0, 160.0], [260.0, 160.0],],

        "map_tiles": {
            "GrassTile": [[300.0, 300.0]],
            "Box": [[400.0, 300.0], [150.0, 500.0]],
        },

        "background": "BackgroundBlue",
    },
}


# level generation data
enemy_types = {
    "Zombie": {"min_stage":0, "class": Zombie},
    "Gunner": {"min_stage":0, "class": Gunner},
    "SelfDestructor": {"min_stage":0, "class": SelfDestructor},
}

background_types = [
    "BackgroundYellow",
    "BackgroundGreen",
    "BackgroundRed",
    "BackgroundBlue",
]

chunk_variants = {
    "V1": {
        "map_tiles": {
            "Box": [],
        },

        "spawnpoints": [],
    }
}

class Level:
    
    def __init__(self, level):
        self.player = None

        if not level in premade_levels:
            self.data = premade_levels[default_level]
        else:
            self.data = premade_levels[level]

    def load_scene(self):

        self.scene = {
            "BACKGROUND": set(),
            "MAP": set(),
            "TO_DRAW": set(),
            "ENEMIES": set(),
            "COLLIDABLE": set(),
            "WITH_GUN": set(),
        }

        if not self.player:
            if not self.load_player(self.data["player"]):
                return False

        # make map
        for tile_type, positions in self.data["map_tiles"].items():
            for pos in positions:
                new_tile = Tile(pos, 0.0, _type=tile_type)
                self.scene["MAP"].add(new_tile)
                self.scene["COLLIDABLE"].add(new_tile)

        # create a raycaster that will work for the current map
        self.raycaster = Raycaster(self.scene["MAP"], self.scene["ENEMIES"])
        self.player.set_raycaster(self.raycaster) # give player a new raycaster

        self.scene["BACKGROUND"].add(self.data["background"])

        for pos in self.data["zombies"]:
            new_zombie = Zombie(pos, 0.0, raycaster=self.raycaster)
            new_zombie.set_target(self.player)
            self.scene["TO_DRAW"].add(new_zombie)
            self.scene["ENEMIES"].add(new_zombie)
            self.scene["COLLIDABLE"].add(new_zombie)

        for pos in self.data["gunners"]:
            new_gunner = Gunner(pos, 0.0, raycaster=self.raycaster)
            new_gunner.set_target(self.player)
            self.scene["TO_DRAW"].add(new_gunner)
            self.scene["ENEMIES"].add(new_gunner)
            self.scene["COLLIDABLE"].add(new_gunner)
            self.scene["WITH_GUN"].add(new_gunner)

        for pos in self.data["gunners"]:
            new_self_destructor = SelfDestructor(pos, 0.0, raycaster=self.raycaster)
            new_self_destructor.set_target(self.player)
            self.scene["TO_DRAW"].add(new_self_destructor)
            self.scene["ENEMIES"].add(new_self_destructor)
            self.scene["COLLIDABLE"].add(new_self_destructor)


    def load_player(self, position=[280.0, 750.0], rotation=-90):
        if self.player or not self.scene:
            return False

        self.player = Player(position, rotation)
        self.scene["TO_DRAW"].add(self.player)
        self.scene["COLLIDABLE"].add(self.player)
        self.scene["WITH_GUN"].add(self.player)

        return True



    def add_projectile(self, projectile):
        self.scene["TO_DRAW"].add(projectile)
        self.scene["COLLIDABLE"].add(projectile)


    def generate_level(self, stage=1):
        pass
