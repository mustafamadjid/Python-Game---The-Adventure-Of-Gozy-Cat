from settings import *
from abc import ABC,abstractmethod
from level import Level
from pytmx.util_pygame import load_pygame
from os.path import join

from support import *

class Game(ABC):
    def __init__(self,width,height,title):
        pygame.init()
        self._width = width
        self._height = height
        self.display_surface = pygame.display.set_mode((self._width,self._height))
        pygame.display.set_caption(title)
       

    @abstractmethod
    def run():
        pass

    @abstractmethod
    def import_assets():
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
        self.import_assets()
        
        self.tmx_map = {0: load_pygame(join('Assets','Map','revisi fatih lagi','File TILED','File TILED','Map and Stage','stage level.tmx'))}
        self.current_stage = Level(self.tmx_map[0],self.level_frames)
        self.clock = pygame.time.Clock()
    
    
    def import_assets(self):
        self.level_frames = {
            'Spike' : import_folder('Assets','Map','revisi fatih lagi','File TILED','File TILED','Spikes'),
            'player' : import_sub_folders('Assets','Player')
        }
        print(self.level_frames['player'])
    
    def run(self):
        while True:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.current_stage.run()
            pygame.display.update()

if __name__ == "__main__":
    game = GozyGame()
    game.run()