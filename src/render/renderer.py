import os, pygame

from .spritesheet import SpriteSheet

class Renderer:
    
    def __init__(self, screen):
        self.entities_sheet = SpriteSheet(os.path.join("assets", "spritesheet_characters.png"))
        self.screen = screen

        self.type_to_sprite = {
            "Player": self.entities_sheet.image_at((164, 88, 49, 43), -1),
        }

    def draw_scene(self, scene):
        
        for object in scene:
            if object._type in self.type_to_sprite:
                
                sprite = self.type_to_sprite[object._type]
                sprite = pygame.transform.rotate(sprite, object.rotation)
                
                rect = sprite.get_rect()
                rect.center = object.position[0], object.position[1]

                self.screen.blit(sprite, rect)