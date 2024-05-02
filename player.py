from pygame.sprite import _Group
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.Surface((143,92))
        self.rect = self.image.get_rect(topleft = pos)
        
        # Movement
        self.direction = vector()
        self.speed = 200
    
    def input(self):
        keys = pygame.key.get_pressed()
        input_vector = vector(0,0)
        
        if keys[pygame.K_RIGHT]:
            input_vector.x += 1
        if keys[pygame.K_LEFT]:
            input_vector.x -= 1
        
        self.direction = input_vector
        if input_vector:
            self.direction = input_vector.normalize()
        else:
            self.direction = input_vector
    
    def move (self,dt):
        self.rect.topleft += self.direction * self.speed * dt
    
    def update(self,dt):
        self.input(dt)
        self.move(dt)