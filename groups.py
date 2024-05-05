from settings import *

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = vector()
    
    def draw(self,target_position):
        self.offset.x = -(target_position[0] - 1280/2)
        self.offset.y = -(target_position[1] - 720/2)
        
        
        for sprite in sorted(self,key=lambda sprite: sprite.z):
            offset_pos = sprite.rect.topleft + self.offset
            self.display_surface.blit(sprite.image,offset_pos)