from settings import *
from sprites import *
from data import *

class AllSprites(pygame.sprite.Group):
    def __init__(self,width,height):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = vector()
        self.width , self.height = width *TILE_SIZE, height *TILE_SIZE
        
        self.borders = {
            'left' : 0,
            'right' : -self.width + 1280,
            'bottom' : -self.height + 720,
            'top' : 0
        }
        
    
    def camera_constraint(self):
        self.offset.x = self.offset.x if self.offset.x < self.borders['left'] else self.borders['left']
        self.offset.x = self.offset.x if self.offset.x > self.borders['right'] else self.borders['right']
        self.offset.y = self.offset.y if self.offset.y > self.borders['bottom'] else self.borders['bottom']
        self.offset.y = self.offset.y if self.offset.y < self.borders['top'] else self.borders['top']
    
    def draw(self,target_position,dt):
        self.offset.x = -(target_position[0] - 1280/2)
        self.offset.y = -(target_position[1] - 720/2)
        self.camera_constraint()
        
        
        for sprite in sorted(self,key=lambda sprite: sprite.z):
            offset_pos = sprite.rect.topleft + self.offset
            self.display_surface.blit(sprite.image,offset_pos)


class WorldSprites(pygame.sprite.Group):
    def __init__(self,data,width,height):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.data = data
        self.offset = vector()
        self.width , self.height = width *TILE_SIZE, height *TILE_SIZE
        
        self.borders = {
            'left' : 0,
            'right' : -self.width + 1280,
            'bottom' : -self.height + 720,
            'top' : 0
        }
        
    
    def camera_constraint(self):
        self.offset.x = self.offset.x if self.offset.x < self.borders['left'] else self.borders['left']
        self.offset.x = self.offset.x if self.offset.x > self.borders['right'] else self.borders['right']
        self.offset.y = self.offset.y if self.offset.y > self.borders['bottom'] else self.borders['bottom']
        self.offset.y = self.offset.y if self.offset.y < self.borders['top'] else self.borders['top']
        
    def draw (self,target_position,dt):
        self.offset.x = -(target_position[0] - 1280/2)
        self.offset.y = -(target_position[1] - 720/2)
        self.camera_constraint()
        
        for sprite in sorted(self,key = lambda sprite: sprite.z):
            if sprite.z == Z_LAYERS['path']:
                if sprite.z <= self.data.unlocked_level:
                    self.display_surface.blit(sprite.image,sprite.rect.topleft + self.offset)
            else:
                self.display_surface.blit(sprite.image,sprite.rect.topleft + self.offset)
