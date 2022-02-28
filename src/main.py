# system
from random import sample
import sys, pygame
from numpy import power
from pygame.locals import *

# services
from .settings import Settings
from .states import ScreenState
from .gui import Gui
from .level import Level
from .render.renderer import Renderer
from .physics.collision_detection import collision_detection

# instancces
from .entities.Projectile import Projectile

POWERUPS = [
    ["SPEED", 1.20],
    ["HEALTH", 1.10],
    ["RECOIL", 0.50],
    ["FIRE RATE", 0.65],
]


class GameState:
    def __init__(self):
        self.screen_state = ScreenState.MAIN_MENU

        self.stage = 0
        self.current_enemies = 0
        self.enemies_left = 0
        self.max_enemies = 0
        self.powerup_indexes = [0, 1]


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
            self._update_game_state()
            
            
            if self.game_state.screen_state == ScreenState.PLAYING:
                self._update(Settings.dt)

            self._render()
            self._game_clock.tick(Settings.fps)


    def _setup_level(self):
        self.level = Level()
        self.level.load_scene(self.game_state)


    def _check_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            
            self.gui.process_event(event)

            if event.type == pygame.USEREVENT:
                if event.user_type == "ENEMY_DIED":
                    self.game_state.current_enemies -= 1
                    self.game_state.enemies_left -= 1


    def _update_game_state(self):

        if self.game_state.screen_state == ScreenState.PLAYER_DIED:
            self.level.load_scene(self.game_state)
            self.game_state.screen_state = ScreenState.MAIN_MENU

        elif self.game_state.enemies_left <= 0:
            self.level.load_scene(self.game_state)
            self.powerup_indexes = sample(range(len(POWERUPS)), 2)
            self.gui.show_powerup(True, POWERUPS[self.powerup_indexes[0]], POWERUPS[self.powerup_indexes[1]])

        elif self.game_state.screen_state == ScreenState.POWERUP1:
            self.level.player.apply_powerup(POWERUPS[self.powerup_indexes[0]])
            self.level.player.health.heal_up(self.level.player.health.max_health)
            self.gui.show_gameplay()

        elif self.game_state.screen_state == ScreenState.POWERUP2:
            self.level.player.apply_powerup(POWERUPS[self.powerup_indexes[0]])
            self.level.player.health.heal_up(self.level.player.health.max_health)
            self.gui.show_gameplay()


        enemies_to_spawn = self.game_state.max_enemies - self.game_state.current_enemies
        while enemies_to_spawn > 0:
            if self.game_state.enemies_left > self.game_state.current_enemies:
                self.level.spawn_enemy(self.game_state)

            enemies_to_spawn -= 1
            

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