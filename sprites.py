# import pygame
from typing import Iterable
from settings import *
from pygame.sprite import AbstractGroup, Group

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
        self.item_type = item_type
        

class Node(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups,level,data,paths):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(center = (pos[0] + TILE_SIZE/2, pos[1] + TILE_SIZE/2))
        self.z = Z_LAYERS['path']
        self.level = level
        self.data = data
        self.paths = paths
    
    def can_move(self,direction):
        if direction in list(self.paths.keys()):
            return True
            
            
class Icon(pygame.sprite.Sprite):
    def __init__(self, pos, groups,frames):
        super().__init__(groups)
        self.path = None
        self.direction = vector()
        self.speed = 2
        
        # Image
        self.frames,self.frame_index = frames , 0
        self.state = 'idle'
        self.image = self.frames[self.state][self.frame_index]
        self.z = Z_LAYERS['main']
        
        # Rect
        self.rect = self.image.get_rect(center = pos)

    def start_move(self,path):
        self.rect.center = path[0]
        self.path = path[1:]
        self.find_path()
    
    def find_path(self):
        if self.path:
            print(self.path)
            if self.rect.centerx == self.path[0][0]: #Vertical
                self.direction = vector(0,1 if self.path[0][1] > self.rect.centery else -1)
            else: #Horizontal
                self.direction = vector(1 if self.path[0][0] > self.rect.centerx else -1,0)
        else:
            self.direction = vector()

    def update(self):
        if self.path:
            self.rect.center += self.direction * self.speed