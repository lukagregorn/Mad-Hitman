# instances
from turtle import pos
from .entities.Player import Player
from .entities.Zombie import Zombie
from .entities.Gunner import Gunner
from .entities.SelfDestructor import SelfDestructor
from .entities.Tile import Tile
from .entities.Spawnpoint import Spawnpoint

from .physics.raycaster import Raycaster
from .render.renderer import Renderer

from random import choice, sample


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

# SCREEN is split into 7 chunks
# bottom chunk is always empty and is where the player spawns
# then we have 6 300x240 chunks where the magic happens
# we pick 3 random chunks that will also have a spawnpoint in them
# items in chunk variants have positions of top left rectangles
chunk_variants = [
    {
        "map_tiles": {
            "Box": [[54,54], [54,108], [54,162], [108,162], [162,162]],
        },

        "spawnpoints": [[128,100]],
    },

    {
        "map_tiles": {
            "Box": [[0,93], [54,93], [108,93], [162,93]],
        },

        "spawnpoints": [[81,29]],
    },

    {
        "map_tiles": dict(),
        "spawnpoints": [[150,100]],
    },

    {
        "map_tiles": {
            "Box": [[162,93]],
        },

        "spawnpoints": [[100,20]],
    },

    {
        "map_tiles": {
            "Box": [[162,100], [216, 100]],
        },

        "spawnpoints": [[20,20]],
    },

    {
        "map_tiles": {
            "Box": [[246,80], [192, 80]],
        },

        "spawnpoints": [[150,150]],
    },

    {
        "map_tiles": {
            "Box": [[140,100], [140, 154]],
        },

        "spawnpoints": [[10,10]],
    },
]

chunk_positions = [
    [0,0], [300,0],
    [0,240], [300,240],
    [0,480], [300,480],
]

class Level:
    
    def __init__(self):
        self.player = None
        self.data = None
        self.scene = None


    def load_scene(self):
        self.destroy_scene()
        self.data = self.generate_level()

        self.scene = {
            "BACKGROUND": set(),
            "MAP": set(),
            "TO_DRAW": set(),
            "ENEMIES": set(),
            "COLLIDABLE": set(),
            "WITH_GUN": set(),
            "SPAWNPOINTS": set(),
        }

        self.load_player(self.data["player"])

        # make map
        for tile_type, positions in self.data["map_tiles"].items():
            for pos in positions:
                new_tile = Tile(pos, 0.0, _type=tile_type)
                self.scene["MAP"].add(new_tile)
                self.scene["COLLIDABLE"].add(new_tile)

        # add spawnpoints
        for pos in self.data["spawnpoints"]:
            new_sp = Spawnpoint(pos)
            self.scene["SPAWNPOINTS"].add(new_sp)

        # create a raycaster that will work for the current map
        self.raycaster = Raycaster(self.scene["MAP"], self.scene["ENEMIES"])
        self.player.set_raycaster(self.raycaster) # give player a new raycaster

        self.scene["BACKGROUND"].add(self.data["background"])
        '''
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
        '''


    def destroy_scene(self):
        if not self.scene:
            return

        for scene_set in self.scene.values():
            scene_set.clear()
            del scene_set

        self.scene.clear()
        self.scene = None


    def load_player(self, position=[280.0, 750.0], rotation=90):
        if not self.scene:
            return False

        if self.player:
            self.player.reset_position(position, rotation)

            if not self.player in self.scene["TO_DRAW"]:
                self.scene["TO_DRAW"].add(self.player)

            if not self.player in self.scene["WITH_GUN"]:
                self.scene["WITH_GUN"].add(self.player)

            if not self.player in self.scene["COLLIDABLE"]:
                self.scene["COLLIDABLE"].add(self.player)

        else:
            self.player = Player(position, rotation)
            self.scene["TO_DRAW"].add(self.player)
            self.scene["COLLIDABLE"].add(self.player)
            self.scene["WITH_GUN"].add(self.player)

        return True



    def add_projectile(self, projectile):
        self.scene["TO_DRAW"].add(projectile)
        self.scene["COLLIDABLE"].add(projectile)


    def generate_level(self, stage=0):
        data = {
            "player": [300.0, 760.0],
            "map_tiles": dict(),
            "spawnpoints": [],
            "background": choice(background_types),
        }

        chunk_spawnpoint_indexes = sample(range(len(chunk_positions)), 3)

        # get random chunk variant for each chunk
        for i in range(len(chunk_positions)):
            random_chunk = choice(chunk_variants)

            # get all tiles
            for tile, positions in random_chunk["map_tiles"].items():
                if not (tile in data["map_tiles"].keys()):
                    data["map_tiles"][tile] = []

                for pos in positions:
                    # transform position to center of image
                    new_pos = [pos[0] + Renderer.image_cords[tile][2]/2 + chunk_positions[i][0], pos[1] + Renderer.image_cords[tile][3]/2 + chunk_positions[i][1]]
                    data["map_tiles"][tile].append(new_pos)

            # check if we need spawnpoints too
            if i in chunk_spawnpoint_indexes:
                for pos in random_chunk["spawnpoints"]:
                    new_pos = [pos[0] + Renderer.image_cords["Spawnpoint"][2]/2 + chunk_positions[i][0], pos[1] + Renderer.image_cords["Spawnpoint"][3]/2 + chunk_positions[i][1]]
                    data["spawnpoints"].append(new_pos)

        return data
