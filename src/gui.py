import pygame_gui, pygame, os

from .settings import Settings 

class Gui:
    
    def __init__(self, screen, game_state):
        self.manager = pygame_gui.UIManager((Settings.screen_width, Settings.screen_height), os.path.join("assets", "gui_theme.json"))
        self.screen = screen
        self.game_state = game_state

        self.ui = {}
        self.make_ui()


    def make_ui(self):
        self.ui["play"] = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((100, 200), (400, 75)),
                                            text='PLAY',
                                            manager=self.manager)

        self.ui["pause"] = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((Settings.screen_width-32-4, 4), (32, 32)),
                                            text='||',
                                            manager=self.manager)
        self.ui["pause"].visible = False

        self.ui["palyer_health"] = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((4, 800-32-4), (64, 32)),
                                            text='HP: 000',
                                            manager=self.manager)
        self.ui["palyer_health"].visible = False


        self.ui["stage"] = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((600-4-64, 800-32-4), (64, 32)),
                                            text='STAGE: 0',
                                            manager=self.manager)
        self.ui["stage"].visible = False

    def process_event(self, event):
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element is self.ui["play"]:
                    self.game_state.menu = False
                    self.ui["play"].visible = False
                    self.ui["pause"].visible = True
                    self.ui["palyer_health"].visible = True
                    self.ui["stage"].visible = True

                if event.ui_element is self.ui["pause"]:
                    self.game_state.menu = True
                    self.ui["play"].visible = True
                    self.ui["pause"].visible = False
                    self.ui["palyer_health"].visible = False
                    self.ui["stage"].visible = False

            if event.user_type == "PLAYER_DIED":
                self.game_state.menu = True     # TODO: reset here
                self.game_state.restart = True

                self.ui["play"].set_text("RESTART")
                self.ui["play"].visible = True

                self.ui["pause"].visible = False
                self.ui["palyer_health"].visible = False
                self.ui["stage"].visible = False

            if event.user_type == "HEALTH_CHANGED":
                self.ui["palyer_health"].set_text(f"HP: {event.player_health}")

            if event.user_type == "STAGE_CHANGED":
                self.ui["stage"].set_text(f"STAGE: {event.stage}")

        self.manager.process_events(event)


    def update(self):
        self.manager.update(Settings.dt)
        self.manager.draw_ui(self.screen)