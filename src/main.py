# system
import sys, pygame, os

# services
from settings import Settings
from level import Level
from render.renderer import Renderer

# instances
from instances.humanoid.player.Player import Player


class MadGunner:

    def __init__(self):
        
        pygame.init()
        
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption(self.settings.window_caption)

        self.renderer = Renderer(self.screen)

    
    def run_game(self):
        self._game_clock = pygame.time.Clock()
        self._setup_level("test")

        while True:
            self._check_events()
            self._update(self.settings.dt)
            self._render()

            self._game_clock.tick(self.settings.fps)


    def _setup_level(self, level):
        self.current_level = Level(level)
        self.current_level.load_scene()


    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    print('left')
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    print('right')
                if event.key == pygame.K_UP or event.key == ord('w'):
                    print('up')
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    print('down')

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    print('left stop')
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    print('right stop')
                if event.key == pygame.K_UP or event.key == ord('w'):
                    print('up stop')
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    print('down stop')


    def _update(self, dt):
        for object in self.current_level.scene:
            object._update(dt)
                


    def _render(self):
        self.screen.fill((255,255,255))

        self.renderer.draw_scene(self.current_level.scene)

        pygame.display.flip()



if __name__ == '__main__':
    game = MadGunner()
    game.run_game()