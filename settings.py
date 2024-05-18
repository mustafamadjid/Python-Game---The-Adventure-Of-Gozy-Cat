import pygame,sys
from pygame.math import Vector2 as vector

TILE_SIZE = 64
ANIMATION_SPEED = 0.15


Z_LAYERS = {
    'bg 1' : 0,
    'bg 2' : 1,
    'bg tiles' : 2,
    'path' : 3,
    'bg details 1' : 4,
    'bg details 2' : 5,
    'bg details 3' : 6,
    'bg details 4' : 7,
    'terrain' : 8,
    'main' : 9,
    'obstacle' : 10,
    'fg' : 11
}
