from settings import *
from abc import ABC,abstractmethod
from level import Level
from pytmx.util_pygame import load_pygame
from os.path import join
from support import *
from data import Data
from ui import UI
from debug import debug
from overworld import *

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
        
        self.ui = UI(self.font, self.ui_frames)
        self.data = Data(self.ui)
        self.tmx_map = {
            0: load_pygame(join('Assets','Map','Stage Level','stage.tmx'))}
        
        
        
        self.tmx_overworld = load_pygame(join('Assets','Map','Map','Aset Tiles','Map Fix.tmx'))
        
        self.current_stage = Overworld(self.tmx_overworld,self.data,self.overworld_frames,self.switch_stage)
        self.current_stage = Level(self.tmx_map[self.data.current_level],self.level_frames,self.audio_files,self.data,self.switch_stage)
        self.clock = pygame.time.Clock()
        
        self.game_active = False
        
        
    
        self.bg_music['ingame music'].play(-1)
        self.bg_music['ingame music'].set_volume(0.5)
        
    
    def switch_stage (self,target,unlock = 0):
        if target == 'level':
            self.current_stage = Level(self.tmx_map[self.data.current_level],self.level_frames,self.audio_files,self.data,self.switch_stage)
            self.bg_music['overworld music'].stop()
            self.bg_music['ingame music'].play(-1)
            self.bg_music['ingame music'].set_volume(0.5)
        else: # Overworld
            if unlock > 0:
                self.data.unlocked_level = unlock
            else:
                self.data.health -= 1
            self.current_stage = Overworld(self.tmx_overworld,self.data,self.overworld_frames,self.switch_stage)
            self.bg_music['ingame music'].stop()
            self.bg_music['overworld music'].play(-1)
            self.bg_music['overworld music'].set_volume(0.5)
            
            
    def import_assets(self):
        self.level_frames = {
            'Spike' : import_folder('Assets','Spikes'),
            'Chicken' : import_folder('Assets','makanan (koin)','Chicken'),
            'Fish' : import_folder('Assets','makanan (koin)','Fish'),
            'Food' : import_folder('Assets','makanan (koin)','Food'),
            'player' : import_sub_folders('Assets','Player'),
            'Slime' : import_folder('Assets','enemy','slime_3'),
            'Fish' : import_folder('Assets','makanan (koin)','Fish'),
            'Food' : import_folder('Assets','makanan (koin)','Food'),
            'Particle' : import_folder('Assets','ui','effect','particle'),
            'Hit' : import_folder('Assets','Player','hit')
        }
        self.font = pygame.font.Font(join('Assets', 'ui', 'runescape_uf.ttf'), 40)

        self.ui_frames = {
			'heart': import_folder('Assets', 'ui', 'heart'), 
			'fish':import_image('Assets', 'ui', 'fish')
		}
        
        self.overworld_frames = {
            'Node' : import_image('Assets','Map','Map','object','1'),
            'Player' : import_sub_folders('Assets','Player'),
        }
        
        self.audio_files = {
            'snack' : pygame.mixer.Sound(join('Assets','Sound','Sound Effect','snack.wav')),
            'jump' : pygame.mixer.Sound(join('Assets','Sound','Sound Effect','jump.wav'))
        }
        
        self.bg_music = {
            'ingame music' : pygame.mixer.Sound(join('Assets','Sound','Music Background','in game.mp3')),
            'overworld music' : pygame.mixer.Sound(join('Assets','Sound','Music Background','overworld music.mp3'))
        }
        
    def game_end(self):
        if self.data.health <= 0:
            # self.display_surface.fill('yellow')
            # self.data.health = 5
            # self.game_active = False
            pygame.quit()
            sys.exit()
    
    def run(self):
        while True:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                else:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        self.game_active = True
                     
                     
            if self.game_active == True:            
                self.current_stage.run()
                self.ui.update()
                self.game_end()
                # self.play_music()
                pygame.display.update()
                debug(self.data.health)
                pygame.display.update()
                        

if __name__ == "__main__":
    game = GozyGame()
    game.run()