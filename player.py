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
        self.gravity = 1
        self.jump = False
        self.jump_height = 20
        
        # collision
        self.collision_sprites =  collision_sprites
        self.on_surface = {'floor': False,'left' : False, 'right': False}
    
    def input(self):
        keys = pygame.key.get_pressed()
        input_vector = vector(0,0)
        
        if keys[pygame.K_RIGHT]:
            input_vector.x += 1
        if keys[pygame.K_LEFT]:
            input_vector.x -= 1
        self.direction.x = input_vector.normalize().x if input_vector else input_vector.x
        
        if keys[pygame.K_SPACE]:
            self.jump = True
    
    def move (self):
        # Horizontal
        self.rect.x += self.direction.x * self.speed
        self.collision('horizontal')
        
        # Vertical
        self.direction.y += self.gravity
        self.rect.y += self.direction.y
        self.collision('vertical')
        
        if self.jump == True:
            if self.on_surface['floor']:
                self.direction.y = -self.jump_height
                self.jump = False
    
    def check_contact(self):
        floor_rect = pygame.Rect(self.rect.bottomleft,(self.rect.width,2))
        collide_rect = [sprite.rect for sprite in self.collision_sprites]
        # right_rect
        # left_rect
        self.on_surface['floor'] = True if floor_rect.collidelist(collide_rect) >= 0 else False  
        
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
                        # top
                        if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                            self.rect.top = sprite.rect.bottom
                        
                        # Bottom
                        if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                            self.rect.bottom = sprite.rect.top
                        self.direction.y = 0
                
                
    def update(self):
        self.old_rect = self.rect.copy()
        self.input()
        self.move()