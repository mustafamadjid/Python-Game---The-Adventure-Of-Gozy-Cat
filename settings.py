import pygame,sys
from pygame.math import Vector2 as vector

TILE_SIZE = 64
ANIMATION_SPEED = 0.15


Z_LAYERS = {
    'bg 1' : 0,
    'bg 2' : 1,
    'bg details 1' : 2,
    'bg details 2' : 3,
    'terrain' : 4,
    'main' : 5
}
# New Comment


# 'pijakan','BG 5 (pohon)','BG 4 (gunung grass)','BG 3 (awan)','BG 2 (rock mt)','BG 1'