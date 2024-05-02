# Komen baru From Me
# oke makasih tha
# Komen baru coba commit dari vs code
# KOmen coba adittttttttt

from settings import *
from abc import ABC,abstractmethod
from level import Level
from pytmx.util_pygame import load_pygame
from os.path import join

class Game(ABC):
    def __init__(self,width,height,title):
        pygame.init()
        self._width = width
        self._height = height
        self.display_surface = pygame.display.set_mode((self._width,self._height))
        pygame.display.set_caption(title)
        
        self.current_stage =Level()
       

    @abstractmethod
    def run():
        pass
    
    @property
    def width(self):
        return self._width
    
    @property
    def height(self):
        return self._height
    
    # @width.setter
    # def width(self,new_width):
    #     self._width = new_width
    

class GozyGame(Game):
    def __init__(self):
        super().__init__(1280,720,'The Adventure of Gozy Cat')
    
    
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()

if __name__ == "__main__":
    game = GozyGame()
    game.run()