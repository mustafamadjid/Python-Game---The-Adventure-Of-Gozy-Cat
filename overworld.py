from settings import *
from sprites import *
from groups import *
from data import *

class Overworld:
    def __init__(self,tmx_map,data,overworld_frames):
        self.display_surface = pygame.display.get_surface()
        self.data = data
        
        # groups
        self.all_sprites = WorldSprites(data,width=tmx_map.width,height=tmx_map.height)
        
        self.setup(tmx_map,overworld_frames)
    
    def setup(self,tmx_map,overworld_frames):
        # Tiles
        for layer in ['Tanah','Welcome bush']:
            for x,y, surf in tmx_map.get_layer_by_name(layer).tiles():
                Sprite((x*TILE_SIZE,y*TILE_SIZE),surf,self.all_sprites,Z_LAYERS['bg tiles'])

        # Object
        for obj in tmx_map.get_layer_by_name('Object'):
            if obj.name in ['Trees','Tree','Wood','Bush','Rock','Node']:
                z = Z_LAYERS['bg tiles']
                Sprite((obj.x,obj.y),obj.image,self.all_sprites,z)
            
        # Nodes and Player
        for obj in tmx_map.get_layer_by_name('Nodes'):
            # Player
            if obj.name == 'Node' and obj.properties['stage'] == self.data.current_level:
                self.icon = Icon(
                    pos = (obj.x + TILE_SIZE/2,obj.y+ TILE_SIZE/2),
                    groups = self.all_sprites,
                    frames = overworld_frames['Player'])
            
            
            # Nodes
            if obj.name == 'Node':
                Node(
                    pos = (obj.x,obj.y),
                    surf = overworld_frames['Node'],
                    groups = self.all_sprites,
                    level = obj.properties['stage'],
                    data = self.data)

        
    def run (self):
        self.all_sprites.update()
        self.all_sprites.draw(self.icon.rect)