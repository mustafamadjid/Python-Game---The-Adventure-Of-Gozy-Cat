from pygame.sprite import Group
from settings import *
from random import choice

class Slime(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups, collision_sprites):
        super().__init__(groups)
        self.frames, self.frame_index = frames, 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)
        self.z = Z_LAYERS['main']
        
        self.direction = choice((-1,1))
        self.collision_rects = [sprite.rect for sprite in collision_sprites]
        self.speed = 200
        
    def update(self):
        # Animasi
        self.frame_index += ANIMATION_SPEED
        self.image = self.frames[int(self.frame_index % len(self.frames))]
        self.image = pygame.transform.flip(self.image, True, False) if self.direction < 0 else self.image
        
        # Moving
        self.rect.x += self.direction * self.speed
        
        # Reverse direction
        floor_rect_right = pygame.FRect(self.rect.bottomright, (1,1))
        floor_rect_left = pygame.FRect(self.rect.bottomleft, (-1,1))
        wall_rect = pygame.FRect(self.rect.topleft + vector(-1,0), (self.rect.width + 2, 1))
        
        if floor_rect_right.pygame.Rect.collidelist(self.collision_rects) < 0 and self.direction > 0 or\
            floor_rect_left.collidelist(self.collision_rects) < 0 and self.direction > 0 or\
                wall_rect.pygame.Rect.collidelist(self.collision_rects) != 1:
            self.direction *= -1