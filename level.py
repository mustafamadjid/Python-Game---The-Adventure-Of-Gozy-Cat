from settings import *
from sprites import *
from player import Player
from groups import AllSprites
from enemy import Slime

class Level:
    def __init__(self,tmx_map,level_frames,audio_files,data,switch_stage):
        self.display_surface = pygame.display.get_surface()
        self.data = data
        self.switch_stage = switch_stage
        
        # Level Data
        self.level_width = tmx_map.width*TILE_SIZE
        self.level_bottom = tmx_map.height*TILE_SIZE
        # tmx_level_properties = tmx_map.get_layer_by_name('Data')[0].properties
        self.level_unlock = 0
    

        for layer in tmx_map.get_layer_by_name('Data'):
            if layer.properties == 'level_unlock':
                self.level_unlock = layer.properties['level_unlock']
        

        # groups
        self.all_sprites = AllSprites(width=tmx_map.width,height=tmx_map.height)
        self.collision_sprites = pygame.sprite.Group()
        self.damage_sprites = pygame.sprite.Group()
        self.slime_sprites = pygame.sprite.Group()
        self.item_sprites = pygame.sprite.Group()
        
        # Frames
        self.particle_frames = level_frames['Particle']
        self.hit_frames = level_frames['Hit']
        
        # Sound
        self.snack_sound = audio_files['snack']
        self.snack_sound.set_volume(0.2)
        self.jump_sound = audio_files['jump']
        self.jump_sound.set_volume(0.2)
        
        # Hit
        # self.hit = False
        
        self.setup(tmx_map,level_frames,audio_files)
        
    def setup(self,tmx_map,level_frames, audio_files):
                  
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
                    frames=level_frames['player'],
                    data = self.data,
                    jump_sound = audio_files['jump'])
            else:
                if obj.name in ('Spike',''):
                    if obj.name == 'Spike':
                        # Sprite((obj.x,obj.y),obj.image,(self.all_sprites,self.collision_sprites))
                        frames = level_frames[obj.name]
                        AnimatedSprite(
                            pos=(obj.x,obj.y),
                            frames=frames,
                            groups = (self.all_sprites,self.damage_sprites),
                            z = Z_LAYERS['obstacle'])
                if obj.name in ('House','Grass'):
                    z = Z_LAYERS['bg details 2']
                    Sprite((obj.x,obj.y),obj.image,self.all_sprites,z)
                    
                    # House succces
                    if obj.name == 'House':
                        self.level_finish_rect = pygame.Rect((obj.x,obj.y),(obj.width,obj.height))
                        
        for obj in tmx_map.get_layer_by_name('Object 2'):
            if obj.name == 'Tree':
                 Sprite((obj.x,obj.y),obj.image,self.all_sprites)
    
        # Enemy
        for obj in tmx_map.get_layer_by_name('Object'):
            if obj.name == 'slime' :
                Slime((obj.x, obj.y), level_frames['Slime'], (self.all_sprites, self.slime_sprites,self.damage_sprites), self.collision_sprites)
    
        # Items
        for obj in tmx_map.get_layer_by_name('Object'):
            if obj.name == 'Fish':
                Item(obj.name, (obj.x + TILE_SIZE / 2, obj.y + TILE_SIZE / 2), level_frames['Fish'], (self.all_sprites, self.item_sprites), self.data)
            if obj.name == 'Food':
                Item(obj.name, (obj.x + TILE_SIZE / 2, obj.y + TILE_SIZE / 2), level_frames['Food'], (self.all_sprites, self.item_sprites),self.data)
    
    def check_constraint(self):
        # left right
        if self.player.rect.left <= 0:
            self.player.rect.left = 0
        if self.player.rect.right >= self.level_width:
            self.player.rect.right = self.level_width
        
        # Bottom border
        if self.player.rect.bottom > self.level_bottom:
            self.switch_stage('overworld',-1)
        
        # Success
        if self.player.rect.colliderect(self.level_finish_rect):
            self.switch_stage('overworld', self.level_unlock)
            
    def hit_collision(self):
        for sprite in self.damage_sprites:
            if sprite.rect.colliderect(self.player.rect):
                self.player.get_damage()
            
    def item_collision(self):
        if self.item_sprites:
            item_sprites = pygame.sprite.spritecollide(self.player, self.item_sprites, True)
            if item_sprites:
                ParticleEffect((item_sprites[0].rect.center),self.particle_frames,self.all_sprites)
                self.snack_sound.play()
                item_sprites[0].activate()
                print(item_sprites[0].item_type)
            
    def run(self):        
        self.all_sprites.update()
        
        self.display_surface.fill('black')
        self.all_sprites.draw(self.player.rect.center)
        self.item_collision()
        self.hit_collision()
        
        self.check_constraint()