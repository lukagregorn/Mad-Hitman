import os, pygame

from spritesheet import SpriteSheet
from settings import Settings

class Renderer:

    image_cords = {
        # entities
        "Player": (164, 88, 49, 43),
        "Zombie": (424, 0, 35, 43),
        "Gunner": (163, 132, 49, 43),
        "SelfDestructor": (423, 44, 35, 43),
        "Boss": (124, 508, 124, 152),
        
        # projectiles
        "ProjectileYellow": (96, 481, 12, 26),
        "ProjectileRed": (120, 481, 12, 26),
        "ProjectileBoss": (60, 481, 12, 26),

        # tiles
        "GrassTile": (0, 128, 128, 128),
        "Box": (1485, 301, 54, 54),

        "Spawnpoint": (1634, 819, 54, 54),

        # decoration (non-collidable)
        "Leaves": (1707, 522, 54, 57),
        "Fikus": (1490, 531, 45, 39),
        "Rock1": (1494, 607, 35, 34),
        "Rock2": (1569, 607, 34, 34),
        "Rock3": (1642, 607, 35, 34),
        "Stick": (1868, 388, 29, 27),
        "TwoBoxes": (1858, 605, 46, 39),
        "Debris1": (1641, 679, 40, 36),
        "Debris2": (1632, 745, 56, 54),
        "Debris3": (1560, 751, 50, 45),
        "Bricks1": (1342, 749, 46, 46),
        "Bricks2": (1425, 759, 21, 27),

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
        self.tank_sheet2 = SpriteSheet(os.path.join("assets", "sheet_tanks2.png"))
        self.backgrounds = SpriteSheet(os.path.join("assets", "backgrounds.png"))
        self.type_to_sprite = {
            "Player": [self.entities_sheet.image_at(self.image_cords["Player"], -1), 0],
            "Zombie": [self.entities_sheet.image_at(self.image_cords["Zombie"], -1), 0],
            "Gunner": [self.entities_sheet.image_at(self.image_cords["Gunner"], -1), 0],
            "SelfDestructor": [self.entities_sheet.image_at(self.image_cords["SelfDestructor"], -1), 0],
            "Boss": [self.tank_sheet2.image_at(self.image_cords["Boss"], -1), 90],

            "ProjectileYellow": [self.tank_sheet.image_at(self.image_cords["ProjectileYellow"], -1), -90],
            "ProjectileRed": [self.tank_sheet.image_at(self.image_cords["ProjectileRed"], -1), -90],
            "ProjectileBoss": [self.tank_sheet.image_at(self.image_cords["ProjectileBoss"], -1), -90],
            "ProjectileBossBig": [self.tank_sheet.image_at(self.image_cords["ProjectileBoss"], -1), -90],

            "GrassTile": [self.tank_sheet.image_at(self.image_cords["GrassTile"], None), 0],
            "Box": [self.spritesheet_tiles.image_at(self.image_cords["Box"], None), 0],

            "Spawnpoint": [self.spritesheet_tiles.image_at(self.image_cords["Spawnpoint"], -1), 0],

            "Leaves" : [self.spritesheet_tiles.image_at(self.image_cords["Leaves"], -1), 0],
            "Fikus" : [self.spritesheet_tiles.image_at(self.image_cords["Fikus"], -1), 0],
            "Rock1" : [self.spritesheet_tiles.image_at(self.image_cords["Rock1"], -1), 0],
            "Rock2" : [self.spritesheet_tiles.image_at(self.image_cords["Rock2"], -1), 0],
            "Rock3" : [self.spritesheet_tiles.image_at(self.image_cords["Rock3"], -1), 0],
            "Stick" : [self.spritesheet_tiles.image_at(self.image_cords["Stick"], -1), 0],
            "TwoBoxes" : [self.spritesheet_tiles.image_at(self.image_cords["TwoBoxes"], -1), 0],
            "Debris1" : [self.spritesheet_tiles.image_at(self.image_cords["Debris1"], -1), 0],
            "Debris2" : [self.spritesheet_tiles.image_at(self.image_cords["Debris2"], -1), 0],
            "Debris3" : [self.spritesheet_tiles.image_at(self.image_cords["Debris3"], -1), 0],
            "Bricks1" : [self.spritesheet_tiles.image_at(self.image_cords["Bricks1"], -1), 0],
            "Bricks2" : [self.spritesheet_tiles.image_at(self.image_cords["Bricks2"], -1), 0],
            
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

        # draw the decoration
        for object in scene["DECORATION"]:
            if object._type in self.type_to_sprite:
                self.draw_object(object)

        
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