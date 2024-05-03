from pygame.sprite import Group
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups,collision_sprites):
        super().__init__(groups)
        self.image = pygame.Surface((143,92))
        self.image.fill('blue')
        
        # Rects
        self.rect = self.image.get_rect(topleft = pos)
        self.old_rect = self.rect.copy()
        
        # Movement
        self.direction = vector()
        self.speed = 5
        self.gravity = 5
        
        # collision
        self.collision_sprites =  collision_sprites
    
    def input(self):
        keys = pygame.key.get_pressed()
        input_vector = vector(0,0)
        
        if keys[pygame.K_RIGHT]:
            input_vector.x += 1
        if keys[pygame.K_LEFT]:
            input_vector.x -= 1
        
        
        self.direction = input_vector.normalize() if input_vector else input_vector
    
    def move (self):
        # Horizontal
        self.rect.x += self.direction.x * self.speed
        self.collision('horizontal')
        
        # Vertical
        self.direction.y += self.gravity
        self.rect.y += self.direction.y
        self.collision('vertical')
        
    def collision(self,axis):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if axis == 'horizontal':
                    # left
                    if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                        self.rect.left = sprite.rect.right
                    # right
                    if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                        self.rect.right = sprite.rect.left
                else:
                    if axis == 'vertical':
                        if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                            self.rect.bottom = sprite.rect.top
                
                
    def update(self):
        self.old_rect = self.rect.copy()
        self.input()
        self.move()