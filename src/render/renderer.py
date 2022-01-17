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
        "Box": (1485, 301, 54, 54),

        "Spawnpoint": (1634, 819, 54, 54),

        # backgrounds
        "BackgroundYellow": (0, 0, 600, 800),
        "BackgroundGreen": (600, 800, 600, 800),
        "BackgroundRed": (600, 0, 600, 800),
        "BackgroundBlue": (0, 800, 600, 800),
    }
    
    def __init__(self, screen):
        self.screen = screen

        self.entities_sheet = SpriteSheet(os.path.join("assets", "spritesheet_characters.png"))
        self.spritesheet_tiles = SpriteSheet(os.path.join("assets", "spritesheet_tiles.png"))
        self.tank_sheet = SpriteSheet(os.path.join("assets", "sheet_tanks.png"))
        self.backgrounds = SpriteSheet(os.path.join("assets", "backgrounds.png"))
        self.type_to_sprite = {
            "Player": [self.entities_sheet.image_at(self.image_cords["Player"], -1), 0],
            "Zombie": [self.entities_sheet.image_at(self.image_cords["Zombie"], -1), 0],
            "Gunner": [self.entities_sheet.image_at(self.image_cords["Gunner"], -1), 0],
            "SelfDestructor": [self.entities_sheet.image_at(self.image_cords["SelfDestructor"], -1), 0],

            "ProjectileYellow": [self.tank_sheet.image_at(self.image_cords["ProjectileYellow"], -1), -90],
            "ProjectileRed": [self.tank_sheet.image_at(self.image_cords["ProjectileRed"], -1), -90],

            "GrassTile": [self.tank_sheet.image_at(self.image_cords["GrassTile"], None), 0],
            "Box": [self.spritesheet_tiles.image_at(self.image_cords["Box"], None), 0],

            "Spawnpoint": [self.spritesheet_tiles.image_at(self.image_cords["Spawnpoint"], -1), 0],

            "BackgroundYellow": [self.backgrounds.image_at(self.image_cords["BackgroundYellow"], None), 0],
            "BackgroundGreen": [self.backgrounds.image_at(self.image_cords["BackgroundGreen"], None), 0],
            "BackgroundRed": [self.backgrounds.image_at(self.image_cords["BackgroundRed"], None), 0],
            "BackgroundBlue": [self.backgrounds.image_at(self.image_cords["BackgroundBlue"], None), 0],
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

        # draw background
        for background in scene["BACKGROUND"]:
            sprite_data = self.type_to_sprite[background]
            sprite = sprite_data[0]

            rect = sprite.get_rect()
            rect.topleft = 0,0
            self.screen.blit(sprite, rect)

        
        # draw the map
        for object in scene["MAP"]:
            if object._type in self.type_to_sprite:
                self.draw_object(object)


        # draw spawnpoints
        for object in scene["SPAWNPOINTS"]:
            if object._type in self.type_to_sprite:
                self.draw_object(object)
                

        # draw entity objects
        for object in scene["TO_DRAW"]:
            if object._type in self.type_to_sprite:
                self.draw_object(object)