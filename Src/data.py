class Data:
    def __init__(self, ui):
        self.ui = ui
        self._score = 0
        self._health = 5
        self.ui.create_hearts(self.health)

        self.unlocked_level = 0
        self.current_level = 0

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        self._score = value
        if self.score >= 100:
            self.score -= 100
            self.health += 1
        self.ui.show_score(self.score)

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