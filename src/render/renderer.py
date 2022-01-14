import os, pygame

from .spritesheet import SpriteSheet

class Renderer:

    image_cords = {
        # entities
        "Player": (164, 88, 49, 43),
        "Zombie": (424, 0, 35, 43),
        "Gunner": (163, 132, 49, 43),
        "SelfDestructor": (423, 44, 35, 43),
        
        # projectiles
        "ProjectileYellow": (96, 481, 12, 26),
        "ProjectileRed": (120, 481, 12, 26),

        # tiles
        "GrassTile": (0, 128, 128, 128),
    }
    
    def __init__(self, screen):
        self.screen = screen

        self.entities_sheet = SpriteSheet(os.path.join("assets", "spritesheet_characters.png"))
        self.tank_sheet = SpriteSheet(os.path.join("assets", "sheet_tanks.png"))
        self.type_to_sprite = {
            "Player": [self.entities_sheet.image_at(self.image_cords["Player"], -1), 0],
            "Zombie": [self.entities_sheet.image_at(self.image_cords["Zombie"], -1), 0],
            "Gunner": [self.entities_sheet.image_at(self.image_cords["Gunner"], -1), 0],
            "SelfDestructor": [self.entities_sheet.image_at(self.image_cords["SelfDestructor"], -1), 0],

            "ProjectileYellow": [self.tank_sheet.image_at(self.image_cords["ProjectileYellow"], -1), -90],
            "ProjectileRed": [self.tank_sheet.image_at(self.image_cords["ProjectileRed"], -1), -90],

            "GrassTile": [self.tank_sheet.image_at(self.image_cords["GrassTile"], None), 0],
        }


    def draw_object(self, object):
        sprite_data = self.type_to_sprite[object._type]
        sprite = sprite_data[0]

        sprite = pygame.transform.scale(sprite, (object.size[0], object.size[1]))
        sprite = pygame.transform.rotate(sprite, object.transform.rotation + sprite_data[1])
        
        rect = sprite.get_rect()
        rect.center = object.transform.position[0], object.transform.position[1]

        self.screen.blit(sprite, rect)


    def draw_scene(self, scene):
        
        # draw the map first
        for object in scene["MAP"]:
            if object._type in self.type_to_sprite:
                self.draw_object(object)
                

        # draw entity objects
        for object in scene["TO_DRAW"]:
            if object._type in self.type_to_sprite:
                self.draw_object(object)