import pygame

#HEIGHT = 720
#WIDTH = 1280

#screen = pygame.display.set_mode((WIDTH, HEIGHT))
#pygame.display.set_caption('Main Menu')

#start_img = pygame.image.load('Assets/Main menu/Start Game.png')
#quit_img = pygame.image.load('Assets/Main menu/Quit.png')

class button():
    def __init__(self,x,y,image,scale):
        widt = image.get_width()
        heig = image.get_height()
        self.image = pygame.transform.scale(image, (int(widt * scale), int(heig * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False
        
    def draw(self, screen):
        action = False
        pos = pygame.mouse.get_pos()
        
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
        
        screen.blit(self.image, (self.rect.x, self.rect.y))
        
        return action
        
#start_button = button(450,320,start_img, 0.65)
#quit_button = button(450,450,quit_img, 0.65)

#bg = pygame.image.load('Assets/Main menu/main bg.png')

#run = True
#while run:
    
    #screen.blit(bg,(0,0))
    
    #if start_button.draw():
        #print('start')
    #if quit_button.draw():
        #run = False
    
    #for event in pygame.event.get():
        #if event.type == pygame.QUIT:
            #run = False
            
    #pygame.display.update()
    
#pygame.quit()