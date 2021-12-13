# system
import sys, pygame, os
from pygame.locals import *

# services
from .settings import Settings
from .level import Level
from .render.renderer import Renderer
from .physics.collision_detection import circle_circle_collision

# instancces
from .entities.Projectile import Projectile


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
            if event.type == QUIT:
                sys.exit()


    def _update(self, dt):
        # update objects
        for object in self.current_level.scene["TO_DRAW"]:
            object._update(dt)

        # check collisions
        for object1 in self.current_level.scene["COLLIDABLE"]:
            for object2 in self.current_level.scene["COLLIDABLE"]:
                if object1 is object2:
                    continue
                
                circle_circle_collision(object1, object2)

        # check for destroyed
        to_destroy = []
        for object in self.current_level.scene["TO_DRAW"]:
            if object.destroyed:
                to_destroy.append(object)

        for object in to_destroy:
            for key in self.current_level.scene:
                if object in self.current_level.scene[key]:
                    self.current_level.scene[key].remove(object)
        
        to_destroy.clear()
        del to_destroy

        # update other stuff
        for object in self.current_level.scene["WITH_GUN"]:
            projectiles = object.gun._update_gun(dt)

            if (len(projectiles) > 0):
                for projectile in projectiles:

                    new_projecitle = Projectile(projectile["position"], projectile["target"], only_hit_types=projectile["only_hit_types"], parent_transform=projectile["parent_transform"], projectile_type=projectile["projectile_type"])
                    self.current_level.add_projectile(new_projecitle)

            object.gun._projectiles_to_spawn = []
                

    def _render(self):
        self.screen.fill((255,255,255))

        self.renderer.draw_scene(self.current_level.scene)

        pygame.display.flip()