from pygame.sprite import Group
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups,collision_sprites):
        super().__init__(groups)
        self.image = pygame.Surface((143,92))
        self.image.fill('blue')
        self.rect = self.image.get_rect(topleft = pos)
        
        # Movement
        self.direction = vector()
        self.speed = 5
        
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
        self.rect.x += self.direction.x * self.speed
        self.collision('horizontal')
        self.rect.y += self.direction.y * self.speed
        self.collision('vertical')
        
    def collision(self,axis):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if axis == 'horizontal':
                    # left
                    if self.rect.left <= sprite.rect.right:
                        self.rect.left = sprite.rect.right
                    # right
                    if self.rect.right >= sprite.rect.left:
                        self.rect.right = sprite.rect.left
                else:
                    pass
                
                
    def update(self):
        self.input()
        self.move()