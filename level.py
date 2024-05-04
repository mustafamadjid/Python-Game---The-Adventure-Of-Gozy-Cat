from settings import *
from sprites import Sprite
from player import Player
from groups import AllSprites

class Level:
    def __init__(self,tmx_map):
        self.display_surface = pygame.display.get_surface()
        
        # groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        
        self.setup(tmx_map)
        
    def setup(self,tmx_map):
        # Object 
        for obj in tmx_map.get_layer_by_name('Object'):
            if obj.name == 'Gozy':
                self.player = Player((obj.x,obj.y),self.all_sprites,self.collision_sprites)
                
        for layer in ['pijakan']:
            # Tiles
            for x,y,surf in tmx_map.get_layer_by_name(layer).tiles():
                Sprite((x * TILE_SIZE,y * TILE_SIZE),surf,(self.all_sprites,self.collision_sprites))
        
        
        
                
    
    def run(self):
        self.all_sprites.update()
        self.display_surface.fill('black')
        self.all_sprites.draw(self.player.rect.center)