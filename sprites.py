# import pygame
from settings import *
from pygame.sprite import Group

class Sprite(pygame.sprite.Sprite):
    def __init__(self,pos,surf = pygame.Surface((TILE_SIZE,TILE_SIZE)),groups = None,z = Z_LAYERS['main']):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.old_rect = self.rect.copy()
        self.z = z

class AnimatedSprite(Sprite):
    def __init__(self,pos,frames,groups,z = Z_LAYERS['main'],animation_speed = 0.1):
        self.frames, self.frame_index = frames, 0
        super().__init__(pos,self.frames[self.frame_index],groups,z)
        self.animation_speed = animation_speed
    
    def animate(self):
        self.frame_index += self.animation_speed
        self.image = self.frames[int(self.frame_index % len(self.frames))]
    
    def update(self):
        self.animate()
        
class Item(AnimatedSprite):
    def __init__(self, item_type, pos, frames, groups):
        super().__init__(pos, frames, groups)
        self.rect.center = pos

