import pygame
from settings import *
from pygame.sprite import Group

class Sprite(pygame.sprite.Sprite):
    def __init__(self,pos,surf = pygame.Surface((TILE_SIZE,TILE_SIZE)),groups = None,z = Z_LAYERS['main']):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.old_rect = self.rect.copy()
        self.z = z