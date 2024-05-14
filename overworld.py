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
        self.node_sprites = pygame.sprite.Group()
        self.setup(tmx_map,overworld_frames)
        
        self.current_node = [node for node in self.node_sprites if node.level == 0][0]
    
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
            
        
        
        # Path
        self.paths = {}
        for obj in tmx_map.get_layer_by_name('Paths'):
            pos = [(int(p.x + TILE_SIZE / 2),int(p.y + TILE_SIZE / 2)) for p in obj.points]
            end = obj.properties['end']
            start = obj.properties['start']
            
            self.paths[end] = {'pos' : pos, 'start' : start}
            
          
          
            
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
                available_paths = {k:v for k,v in obj.properties.items() if k in ('left','right','up','down')}
                print(available_paths)
                Node(
                    pos = (obj.x,obj.y),
                    surf = overworld_frames['Node'],
                    groups = (self.all_sprites,self.node_sprites),
                    level = obj.properties['stage'],
                    data = self.data,
                    paths = available_paths)

        
    def input (self):
        keys = pygame.key.get_pressed()
        if self.current_node:
            if keys[pygame.K_DOWN] and self.current_node.can_move('down'):
                self.move('down')
    
    def move (self,direction):
        path_key = int(self.current_node.paths[direction][0])
        path_reverse = True if self.current_node.paths[direction][-1] == 'r' else False
        path = self.paths[path_key]['pos'][:] if not path_reverse else self.paths[path_key]['pos'][::-1]
        self.icon.start_move(path)
        
    def run (self):
        self.input()
        self.all_sprites.update()
        self.all_sprites.draw(self.icon.rect)