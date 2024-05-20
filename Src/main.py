import pygame
from settings import *
from abc import ABC, abstractmethod
from level import Level
from pytmx.util_pygame import load_pygame
from os.path import join
from support import *
from data import Data
from ui import UI
from menu import Button
from overworld import *

class Game(ABC):
    def __init__(self, width, height, title):
        pygame.init()
        self._width = width
        self._height = height
        self.display_surface = pygame.display.set_mode((self._width, self._height), pygame.RESIZABLE)
        pygame.display.set_caption(title)

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def import_assets(self):
        pass

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

class GozyGame(Game):
    def __init__(self):
        super().__init__(1280, 720, 'The Adventure of Gozy Cat')
        self.import_assets()

        self.hasActivated = False
        self.ui = UI(self.font, self.ui_frames)
        self.data = Data(self.ui)
        self.tmx_map = {
            0: load_pygame(join('..','Assets', 'Map', 'Stage Level 2', 'stage level 2.tmx')),
            1: load_pygame(join('..','Assets', 'Map', 'Stage Level', 'stage.tmx')),
            2: load_pygame(join('..','Assets', 'Map', 'Stage Level 3', 'stage 3.tmx'))
        }

        self.tmx_overworld = load_pygame(join('..','Assets', 'Map', 'Map', 'Aset Tiles', 'Map Fix.tmx'))

        self.current_stage = Overworld(self.tmx_overworld, self.data, self.overworld_frames, self.switch_stage)
        self.clock = pygame.time.Clock()

        self.game_active = False
        self.change_music("main menu.ogg")

    def switch_stage(self, target, unlock=0):
        if target == 'level':
            self.current_stage = Level(self.tmx_map[self.data.current_level], self.level_frames, self.audio_files, self.data, self.switch_stage)
            self.change_music("in game.mp3")
        else:  # Overworld
            if unlock > 0:
                self.data.unlocked_level = unlock
            else:
                self.data.health -= 1

            self.current_stage = Overworld(self.tmx_overworld, self.data, self.overworld_frames, self.switch_stage)
            self.change_music("overworld music.mp3")

    def import_assets(self):
        self.level_frames = {
            'Spike': import_folder('..','Assets', 'Map', 'Stage Level', 'Stage Tiles', 'Spikes'),
            'Chicken': import_folder('..','Assets', 'makanan (koin)', 'Chicken'),
            'Fish': import_folder('..','Assets', 'makanan (koin)', 'Fish'),
            'Food': import_folder('..','Assets', 'makanan (koin)', 'Food'),
            'player': import_sub_folders('..','Assets', 'Player'),
            'Slime_2': import_folder('..','Assets', 'enemy', 'slime_2'),
            'Slime_3': import_folder('..','Assets', 'enemy', 'slime_3'), 
            'Fish': import_folder('..','Assets', 'makanan (koin)', 'Fish'),
            'Food': import_folder('..','Assets', 'makanan (koin)', 'Food'),
            'Particle': import_folder('..','Assets', 'ui', 'effect', 'particle'),
            'Hit': import_folder('..','Assets', 'Player', 'hit'),
            'House' : import_image('..','Assets','rumah','rumah_2','120 x 104'),
            'Skeleton' : import_folder('..','Assets','enemy','skeleton','animate_skeleton')
        }
        self.font = pygame.font.Font(join('..','Assets', 'ui', 'runescape_uf.ttf'), 40)

        self.ui_frames = {
            'heart': import_folder('..','Assets', 'ui', 'heart'),
            'fish': import_image('..','Assets', 'ui', 'fish')
        }

        self.overworld_frames = {
            'Node': import_image('..','Assets', 'Map', 'Map', 'object', '1'),
            'Player': import_sub_folders('..','Assets', 'Player'),
        }

        self.audio_files = {
            'snack': pygame.mixer.Sound(join('..','Assets', 'Sound', 'Sound Effect', 'snack.wav')),
            'jump': pygame.mixer.Sound(join('..','Assets', 'Sound', 'Sound Effect', 'jump.wav'))
        }

    def change_music(self, musicName: str):
        pygame.mixer.music.load(join('..','Assets', 'Sound', 'Music Background', musicName))
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

    def game_end(self):
        if self.data.health <= 0:
            pygame.quit()
            sys.exit()

    def run(self):
        start_img = pygame.image.load('../Assets/Main menu/Start Game.png')
        quit_img = pygame.image.load('../Assets/Main menu/Quit.png')
        start_button = Button(450, 320, start_img, 0.65)
        quit_button = Button(450, 450, quit_img, 0.65)
        bg = pygame.image.load('../Assets/Main menu/main bg.png')
        pygame.mixer.music.play(-1)
        pygame.display.set_icon(pygame.image.load('../Assets/Player/idle/1.png'))

        while True:
            self.display_surface.blit(bg, (0, 0))

            if start_button.draw(self.display_surface):
                self.game_active = True
            if quit_button.draw(self.display_surface):
                pygame.quit()
                sys.exit()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.game_active = True
                elif event.type == pygame.VIDEORESIZE:
                    self._width, self._height = event.w, event.h
                    self.display_surface = pygame.display.set_mode((self._width, self._height), pygame.RESIZABLE)

            if self.game_active and self.game_active != self.hasActivated:
                self.change_music("overworld music.mp3")
                self.hasActivated = True

            if self.game_active:
                self.current_stage.run()
                self.ui.update()
                self.game_end()

            pygame.display.update()
            self.clock.tick(60)

if __name__ == "__main__":
    game = GozyGame()
    game.run()
