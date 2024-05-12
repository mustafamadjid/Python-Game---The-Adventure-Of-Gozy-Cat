from settings import *
from sprites import Sprite, AnimatedSprite, Item
from player import Player
from groups import AllSprites
from enemy import Slime

class Level:
    def __init__(self,tmx_map,level_frames):
        self.display_surface = pygame.display.get_surface()
        
        # Level Data
        self.level_width = tmx_map.width*TILE_SIZE
        self.level_bottom = tmx_map.height*TILE_SIZE
        
        
        # groups
        self.all_sprites = AllSprites(width=tmx_map.width,height=tmx_map.height)
        self.collision_sprites = pygame.sprite.Group()
        self.damage_sprites = pygame.sprite.Group()
        self.slime_sprites = pygame.sprite.Group()
        
        self.setup(tmx_map,level_frames)
        
    def setup(self,tmx_map,level_frames):
                  
        for layer in ['Pijakan','BG 5 (grass mt 2)','BG 4 (grass mt)','BG 3 (rck mt)','BG 2 (awan)','BG 1']:
            # Tiles
            for x,y,surf in tmx_map.get_layer_by_name(layer).tiles():
                groups = [self.all_sprites]
                if layer == 'Pijakan' :
                    groups.append(self.collision_sprites)
                match layer:
                    case 'BG 1' : z = Z_LAYERS['bg 1']
                    case 'BG 5 (grass mt 2)' : z = Z_LAYERS['bg 2']
                    case 'BG 2 (awan)' : z = Z_LAYERS['bg details 1']
                    case 'BG 4 (grass mt)' : z = Z_LAYERS['bg details 1']
                    case 'BG 3 (rck mt)' : z = Z_LAYERS['bg details 2']
                    case 'Pijakan' : z = Z_LAYERS['main']
                Sprite((x * TILE_SIZE,y * TILE_SIZE),surf,groups,z)

        
    
        # Object 
        for obj in tmx_map.get_layer_by_name('Object'):
            if obj.name == 'Gozy':
                self.player = Player(
                    pos = (obj.x,obj.y),
                    groups=self.all_sprites,
                    collision_sprites=self.collision_sprites,
                    frames=level_frames['player'])
            else:
                if obj.name in ('Spike',''):
                    if obj.name == 'Spike':
                        # Sprite((obj.x,obj.y),obj.image,(self.all_sprites,self.collision_sprites))
                        frames = level_frames[obj.name]
                        AnimatedSprite((obj.x,obj.y),frames,(self.all_sprites,self.collision_sprites))
                if obj.name in ('House','Flag'):
                    z = Z_LAYERS['bg details 2']
                    Sprite((obj.x,obj.y),obj.image,self.all_sprites,z)
                    
                    # Flag Succes
                    if obj.name == 'Flag':
                        self.level_finish_rect = pygame.Rect((obj.x,obj.y),(obj.width,obj.height))
                        
        for obj in tmx_map.get_layer_by_name('Object 2'):
            if obj.name == 'Tree':
                 Sprite((obj.x,obj.y),obj.image,self.all_sprites)
    
        # Enemy
        for obj in tmx_map.get_layer_by_name('Object'):
            if obj.name == 'slime' :
                Slime((obj.x, obj.y), level_frames['Slime'], (self.all_sprites, self.slime_sprites), self.collision_sprites)
    
        # # Items
        # for obj in tmx_map.get_layer_by_name('Object'):
        #     Item(obj.name, (obj.x + TILE_SIZE / 2, obj.y), level_frames['Fish'], self.all_sprites)
    
    def check_constraint(self):
        # left right
        if self.player.rect.left <= 0:
            self.player.rect.left = 0
        if self.player.rect.right >= self.level_width:
            self.player.rect.right = self.level_width
        
        # Bottom border
        if self.player.rect.bottom > self.level_bottom:
            print("Yah Mati")
            sys.exit()
        
        # Success
        if self.player.rect.colliderect(self.level_finish_rect):
            print('Success')
            
        
    def run(self):        
        self.all_sprites.update()
        self.display_surface.fill('black')
        self.all_sprites.draw(self.player.rect.center)
        
        self.check_constraint()