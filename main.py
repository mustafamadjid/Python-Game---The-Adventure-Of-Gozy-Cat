import pygame

class Game:
    def __init__(self):
        pygame.init()
        self.width = 600
        self.height = 600
        self.screen = pygame.display.set_mode([self.width, self.height], pygame.RESIZABLE)
        self.screen.fill((255, 255, 255))
        pygame.display.set_caption("The Adventure of Gozy Cat")
        self.clock = pygame.time.Clock()
        self.running = True
        self.resizing = False

    def run(self):
        while self.running:
            self.clock.tick(60)
            for event in pygame.event.get():
                self.handle_event(event)
            self.update()
            self.render()
        pygame.quit()

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.VIDEORESIZE:
            self.handle_resize(event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.resizing = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.resizing = False
        elif event.type == pygame.MOUSEMOTION:
            if self.resizing:
                width, height = pygame.display.get_window_size()
                x, y = event.rel
                width += x
                height += y
                if width < 200:
                    width = 200
                if height < 200:
                    height = 200
                self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
                self.screen.fill((255, 255, 255))

    def handle_resize(self, event):
        self.width, self.height = event.size
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        self.screen.fill((255, 255, 255))

    def update(self):
        pass

    def render(self):
        pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.run()