# instances
from instances.humanoid.enemy.Zombie import Zombie
from instances.humanoid.player.Player import Player

# defaults
default_level = "test"
premade_levels = {
    "test": {
        "player": {"position": [300.0, 400.0], "rotation":-110.0},
        "zombies": [[100.0, 100.0]]
    },
}


class Level:
    
    def __init__(self, level):
        if not level in premade_levels:
            self.data = premade_levels[default_level]
        else:
            self.data = premade_levels[level]

    def load_scene(self):
        self.scene = []

        player = Player("Player", self.data["player"]["position"], self.data["player"]["rotation"], 100)
        self.scene.append(player)

        for pos in self.data["zombies"]:
            new_zombie = Zombie("Zombie", pos, 0.0, 100)
            new_zombie.set_target(player)
            self.scene.append(new_zombie)