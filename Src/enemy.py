from pygame.sprite import Group
from settings import *
from random import choice

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups, collision_sprites):
        super().__init__(groups)
        self.frames, self.frame_index = frames, 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)
        self.z = Z_LAYERS['enemy']

        self.direction = choice((-1,1))
        self.collision_rects = [sprite.rect for sprite in collision_sprites]
        self.speed = 1
        
        
    def update (self):
        # Animate
        self.frame_index += ANIMATION_SPEED - 0.04
        self.image = self.frames[int(self.frame_index) % len(self.frames) ]
        
        if self.direction < 0:
            self.image = pygame.transform.flip(self.image,True,False)
        
        # Move
        self.rect.x += self.direction * self.speed
        
        # Reverse direction
        
        floor_rect_right = pygame.Rect(self.rect.bottomright,(1,1))
        floor_rect_left = pygame.Rect(self.rect.bottomleft,(-1,1))
        
        if floor_rect_right.collidelist(self.collision_rects) < 0 and self.direction > 0:
            self.direction = -1
        elif floor_rect_left.collidelist(self.collision_rects) < 0 and self.direction < 0:
            self.direction = 1
                
                # floor_rect_left.collidelist(self.collision_rects) < 0 and self.direction < 0: