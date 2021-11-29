import os, pygame

from .spritesheet import SpriteSheet

class Renderer:
    
    def __init__(self, screen):
        self.entities_sheet = SpriteSheet(os.path.join("assets", "spritesheet_characters.png"))
        self.tank_sheet = SpriteSheet(os.path.join("assets", "sheet_tanks.png"))
        self.screen = screen

        self.type_to_sprite = {
            "Player": [self.entities_sheet.image_at((164, 88, 49, 43), -1), 0, (1.1, 1.1)],
            "Zombie": [self.entities_sheet.image_at((424, 0, 35, 43), -1), 0, (1.1, 1.1)],
            "Projectile": [self.tank_sheet.image_at((96, 481, 12, 26), -1), -90, (0.75, 0.75)],
        }


    def set_class_sizes(self, classes):
        for c in classes:
            if c._type in self.type_to_sprite:

                sprite_data = self.type_to_sprite[c._type]
                sprite = sprite_data[0]

                (sprite_x, sprite_y) = sprite.get_size()
                sprite = pygame.transform.scale(sprite, (sprite_x * sprite_data[2][0], sprite_y * sprite_data[2][1]))

                (sprite_x, sprite_y) = sprite.get_size()
                c.size = [sprite_x, sprite_y]



    def draw_scene(self, scene):
        
        # objects with transform
        for object in scene["TO_DRAW"]:
            if object._type in self.type_to_sprite:
                
                sprite_data = self.type_to_sprite[object._type]
                sprite = sprite_data[0]

                (sprite_x, sprite_y) = sprite.get_size()
                
                sprite = pygame.transform.scale(sprite, (sprite_x * sprite_data[2][0], sprite_y * sprite_data[2][1]))
                sprite = pygame.transform.rotate(sprite, object.transform.rotation + sprite_data[1])
                
                rect = sprite.get_rect()
                rect.center = object.transform.position[0], object.transform.position[1]

                self.screen.blit(sprite, rect)