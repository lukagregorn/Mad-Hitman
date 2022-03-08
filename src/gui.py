import pygame_gui, pygame, os

from .settings import Settings
from .states import ScreenState

class Gui:
    
    def __init__(self, screen, game_state):
        self.manager = pygame_gui.UIManager((Settings.screen_width, Settings.screen_height), os.path.join("assets", "gui_theme.json"))
        self.screen = screen
        self.game_state = game_state

        self.ui = {}
        self.make_ui()
        self.show_main()


    def make_ui(self):
        self.ui["play"] = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((40, 400), (Settings.screen_width-80, 100)),
                                            text='PLAY',
                                            manager=self.manager)


        self.ui["pause"] = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((Settings.screen_width-32-4, 4), (32, 32)),
                                            text='||',
                                            manager=self.manager)
        self.ui["pause"].visible = False


        self.ui["palyer_health"] = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((4, Settings.screen_height-32-4), (64, 32)),
                                            text='HP: 000',
                                            manager=self.manager)
        self.ui["palyer_health"].visible = False


        self.ui["stage"] = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((Settings.screen_width-4-96, Settings.screen_height-32-4), (96, 32)),
                                            text='STAGE: 0',
                                            manager=self.manager)
        self.ui["stage"].visible = False


        self.ui["main_label"] = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((40, 350), (Settings.screen_width-80, 50)),
                                            text='LABEL',
                                            manager=self.manager)
        self.ui["main_label"].visible = False


        self.ui["pow1"] = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((40, 440), (240, 120)),
                                            text='POW1',
                                            manager=self.manager)
        self.ui["pow1"].visible = False


        self.ui["pow2"] = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((40+40+240, 440), (240, 120)),
                                            text='POW2',
                                            manager=self.manager)
        self.ui["pow2"].visible = False


        self.ui["sound"] = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((Settings.screen_width-92-64-16, 4), (92, 32)),
                                            text=f'Sound: {Settings.sound_volume}',
                                            manager=self.manager)
        self.ui["sound"].visible = False

        self.ui["sound_up"] = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((Settings.screen_width-64-8, 4), (32, 32)),
                                            text='+',
                                            manager=self.manager)
        self.ui["sound_up"].visible = False

        self.ui["sound_down"] = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((Settings.screen_width-32-4, 4), (32, 32)),
                                            text='-',
                                            manager=self.manager)

        self.ui["sound_down"].visible = False

        self.ui["music"] = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((Settings.screen_width-92-64-16, 4+32+4), (92, 32)),
                                            text=f'Music: {Settings.music_volume}',
                                            manager=self.manager)
        self.ui["music"].visible = False

        self.ui["music_up"] = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((Settings.screen_width-64-8, 4+32+4), (32, 32)),
                                            text='+',
                                            manager=self.manager)
        self.ui["music_up"].visible = False

        self.ui["music_down"] = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((Settings.screen_width-32-4, 4+32+4), (32, 32)),
                                            text='-',
                                            manager=self.manager)

        self.ui["music_down"].visible = False


    def process_event(self, event):
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element is self.ui["play"]:
                    
                    if self.game_state.screen_state == ScreenState.MAIN_MENU:
                        self.show_gameplay()

                    if self.game_state.screen_state == ScreenState.PAUSED:
                        self.show_gameplay()                      

                    if self.game_state.screen_state == ScreenState.GAME_OVER:
                        self.show_main(ScreenState.PLAYER_DIED)

                if event.ui_element is self.ui["pause"]:
                    self.show_paused()


                is_volume = False
                if event.ui_element is self.ui["sound_up"]:
                    Settings.sound_volume = max(min(Settings.sound_volume+1, 100), 0)
                    is_volume = True

                if event.ui_element is self.ui["sound_down"]:
                    Settings.sound_volume = max(min(Settings.sound_volume-1, 100), 0)
                    is_volume = True

                if event.ui_element is self.ui["music_up"]:
                    Settings.music_volume = max(min(Settings.music_volume+1, 100), 0)
                    pygame.mixer.music.set_volume(Settings.music_volume/100)
                    is_volume = True

                if event.ui_element is self.ui["music_down"]:
                    Settings.music_volume = max(min(Settings.music_volume-1, 100), 0)
                    pygame.mixer.music.set_volume(Settings.music_volume/100)
                    is_volume = True

                if is_volume:
                    self.show_volume(True)


                if event.ui_element is self.ui["pow1"]:
                    self.show_powerup(False)
                    self.game_state.screen_state = ScreenState.POWERUP1

                if event.ui_element is self.ui["pow2"]:
                    self.show_powerup(False)
                    self.game_state.screen_state = ScreenState.POWERUP2


            if event.user_type == "PLAYER_DIED":
                self.show_game_over()

            if event.user_type == "HEALTH_CHANGED":
                self.ui["palyer_health"].set_text(f"HP: {event.player_health:.0f}")

            if event.user_type == "STAGE_CHANGED":
                self.ui["stage"].set_text(f"STAGE: {event.stage}")

        self.manager.process_events(event)

    
    def set_gameplay_overlay_visible(self, visible=True):
        self.ui["pause"].visible = visible
        self.ui["palyer_health"].visible = visible
        self.ui["stage"].visible = visible


    def show_main(self, with_state=ScreenState.MAIN_MENU):
        self.ui["main_label"].set_text("Survive as long as possible! Enemies ahead!")
        self.ui["main_label"].visible = True
        self.ui["play"].set_text("PLAY")
        self.ui["play"].visible = True
        self.set_gameplay_overlay_visible(False)
        self.game_state.screen_state = with_state


    def show_gameplay(self):
        self.ui["play"].visible = False
        self.ui["main_label"].visible = False
        self.set_gameplay_overlay_visible(True)
        self.game_state.screen_state = ScreenState.PLAYING
        self.show_volume(False)


    def show_paused(self):
        self.ui["play"].set_text("RESUME")
        self.ui["play"].visible = True
        self.set_gameplay_overlay_visible(False)
        self.game_state.screen_state = ScreenState.PAUSED
        self.show_volume(True)


    def show_volume(self, visible):
        self.ui["sound"].visible = visible
        self.ui["sound_up"].visible = visible
        self.ui["sound_down"].visible = visible
        self.ui["sound"].set_text(f"Sound: {Settings.sound_volume}")

        self.ui["music"].visible = visible
        self.ui["music_up"].visible = visible
        self.ui["music_down"].visible = visible
        self.ui["music"].set_text(f"Music: {Settings.music_volume}")


    def show_game_over(self):
        self.ui["play"].set_text("RETRY")
        self.ui["play"].visible = True
        self.ui["main_label"].set_text("GAME OVER!")
        self.ui["main_label"].visible = True
        self.game_state.screen_state = ScreenState.GAME_OVER

    
    def show_powerup(self, visible, powerup1=None, powerup2=None):
        if visible:
            self.ui["main_label"].set_text("Select an upgrade ...")
            self.ui["pow1"].set_text(f"UPGRADE {powerup1[0]}: X{powerup1[1]}")
            self.ui["pow2"].set_text(f"UPGRADE {powerup2[0]}: X{powerup2[1]}")

        self.ui["main_label"].visible = visible
        self.ui["pow1"].visible = visible
        self.ui["pow2"].visible = visible

        self.set_gameplay_overlay_visible(False)
        self.game_state.screen_state = ScreenState.GIVE_POWERUP


    def update(self):
        self.manager.update(Settings.dt)
        self.manager.draw_ui(self.screen)