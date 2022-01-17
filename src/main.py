# system
import sys, os, pygame
from pygame.locals import *

# services
from .settings import Settings
from .gui import Gui
from .level import Level
from .render.renderer import Renderer
from .physics.collision_detection import collision_detection

# instancces
from .entities.Projectile import Projectile


class GameState:
    def __init__(self):
        self.paused = False
        self.menu = True
        self.restart = False
        self.load_new_level = False


class MadGunner:

    def __init__(self):
        
        pygame.init()
        self.game_state = GameState()
        
        self.screen = pygame.display.set_mode((Settings.screen_width, Settings.screen_height))
        self.gui = Gui(self.screen, self.game_state)
        pygame.display.set_caption(Settings.window_caption)

        self.renderer = Renderer(self.screen)

        
    def run_game(self):
        self._game_clock = pygame.time.Clock()
        self._setup_level()

        while True:
            self._check_events()
            
            if self.game_state.load_new_level:
                self.game_state.load_new_level = False
                self.level.load_scene()

            if not self.game_state.menu and not self.game_state.paused:
                self._update(Settings.dt)

            self._render()
            self._game_clock.tick(Settings.fps)


    def _setup_level(self):
        self.level = Level()
        self.level.load_scene()


    def _check_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            
            self.gui.process_event(event)


    def _update(self, dt):
        # update objects
        for object in self.level.scene["TO_DRAW"]:
            object._update(dt)

        # check collisions
        for object1 in self.level.scene["COLLIDABLE"] | self.level.scene["MAP"]:

            # only check active objects as obj1 (we dont want to check static with static ever)
            if object1.rigidBody.static:
                continue

            for object2 in self.level.scene["COLLIDABLE"]:
                if object1 is object2:
                    continue
                
                collision_detection(object1, object2)

        # check for destroyed
        to_destroy = []
        for object in self.level.scene["TO_DRAW"]:
            if object.destroyed:
                to_destroy.append(object)

        for object in to_destroy:
            for key in self.level.scene:
                if object in self.level.scene[key]:
                    self.level.scene[key].remove(object)
        
        to_destroy.clear()
        del to_destroy

        # update other stuff
        for object in self.level.scene["WITH_GUN"]:
            projectiles = object.gun._update_gun(dt)

            if (len(projectiles) > 0):
                for projectile in projectiles:

                    new_projecitle = Projectile(projectile["position"], projectile["target"], only_hit_types=projectile["only_hit_types"], parent_transform=projectile["parent_transform"], projectile_type=projectile["projectile_type"])
                    self.level.add_projectile(new_projecitle)

            object.gun._projectiles_to_spawn = []
                

    def _render(self):
        self.screen.fill((255,255,255))
        self.renderer.draw_scene(self.level.scene)

        self.gui.update()
        pygame.display.flip()