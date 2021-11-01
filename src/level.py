# instances
from instances.humanoid.player.Player import Player

# defaults
default_level = "test"
premade_levels = {
    "test": {
        "player": {"position": [300.0, 400.0], "rotation":-110.0},
        "enemies": {
            "positions": [[90.0,90.0], [100.0, 200.0], [250.0, 300.0], [100.0, 40.0]],
        },
    },
}


class Level:
    
    def __init__(self, level):
        if not level in premade_levels:
            self.data = premade_levels[default_level]
        else:
            self.data = premade_levels[level]

    def load_scene(self):
        print(self.data)
        self.scene = {
            Player("Player", self.data["player"]["position"], self.data["player"]["rotation"], 100),
        }