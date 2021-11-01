class Settings:
    
    def __init__(self):
        # meta
        self._version = 1

        # screen
        self.screen_width = 800
        self.screen_height = 800

        self.window_caption = f"Mad Gunner (V{self._version})"

        # gameplay
        self.fps = 60
        self.dt = 1/self.fps
