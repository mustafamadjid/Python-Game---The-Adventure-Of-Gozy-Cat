import pygame,sys
from pygame.math import Vector2 as vector

TILE_SIZE = 64
ANIMATION_SPEED = 0.1


Z_LAYERS = {
    'bg' : 0,
    'bg details 1' : 1,
    'bg details 2' : 2,
    'terrain' : 3,
    'main' : 4
}
# New Comment


# 'pijakan','BG 5 (pohon)','BG 4 (gunung grass)','BG 3 (awan)','BG 2 (rock mt)','BG 1'