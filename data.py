class Data:
    def __init__(self, ui):
        self.ui = ui
        self._fish = 0
        self._health = 5
        self.ui.create_hearts(self.health)

        self.unlocked_level = 0
        self.current_level = 0

    @property
    def fish(self):
        return self._fish

    @fish.setter
    def fish(self, value):
        self._fish = value
        if self.fish >= 100:
            self.fish -= 100
            self.health += 1
        self.ui.show_fish(self.fish)

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        if self._health > 5:
            self._health = 5
        else:
            self._health = value
            self.ui.create_hearts(value)