from settings import *

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = vector()
        
    
    def camera_constraint(self):
        self.offset.x = self.offset.x if self.offset.x < 0 else 0
    
    def draw(self,target_position):
        self.offset.x = -(target_position[0] - 1280/2)
        self.offset.y = -(target_position[1] - 720/2)
        self.camera_constraint()
        
        
        for sprite in sorted(self,key=lambda sprite: sprite.z):
            offset_pos = sprite.rect.topleft + self.offset
            self.display_surface.blit(sprite.image,offset_pos)