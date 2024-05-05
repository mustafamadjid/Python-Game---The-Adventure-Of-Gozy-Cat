from settings import *
from sprites import Sprite
from player import Player
from groups import AllSprites

class Level:
    def __init__(self,tmx_map,level_frames):
        self.display_surface = pygame.display.get_surface()
        
        # groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        
        self.setup(tmx_map,level_frames)
        
    def setup(self,tmx_map,level_frames):
        # Object 
        for obj in tmx_map.get_layer_by_name('Object'):
            if obj.name == 'Gozy':
                self.player = Player((obj.x,obj.y),self.all_sprites,self.collision_sprites)
            else:
                if obj.name in ('Spike',''):
                    Sprite((obj.x,obj.y),obj.image,(self.all_sprites,self.collision_sprites))
                
                  
        for layer in ['pijakan','BG 5 (pohon)','BG 4 (gunung grass)','BG 3 (awan)','BG 2 (rock mt)','BG 1']:
            # Tiles
            for x,y,surf in tmx_map.get_layer_by_name(layer).tiles():
                groups = [self.all_sprites]
                if layer == 'pijakan' :
                    groups.append(self.collision_sprites)
                match layer:
                    case 'BG 1' : z = Z_LAYERS['bg']
                    case 'BG 2 (rock mt)' : z = Z_LAYERS['bg details 1']
                    case 'BG 3 (awan)' : z = Z_LAYERS['bg details 1']
                    case 'BG 4 (gunung grass)' : z = Z_LAYERS['bg details 2']
                    case 'BG 5 (pohon)' : z = Z_LAYERS['bg details 2']
                    case 'pijakan' : z = Z_LAYERS['main']
                Sprite((x * TILE_SIZE,y * TILE_SIZE),surf,groups,z)

        
        
    def run(self):
        self.all_sprites.update()
        self.display_surface.fill('black')
        self.all_sprites.draw(self.player.rect.center)