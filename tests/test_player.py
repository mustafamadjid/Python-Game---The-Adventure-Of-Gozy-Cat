import unittest
import pygame
from src.player import Player

# Mock classes
class MockSprite(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.rect = pygame.Rect(pos, (50, 50))
        self.old_rect = self.rect.copy()

class MockData:
    def __init__(self):
        self.health = 3

class MockSound:
    def play(self):
        pass

# Unit tests
class TestPlayer(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.mock_sprites = pygame.sprite.Group()
        self.mock_collision_sprites = pygame.sprite.Group(MockSprite((0, 0)))
        self.mock_frames = {'idle': [pygame.Surface((50, 50))], 'run': [pygame.Surface((50, 50))]}
        self.mock_data = MockData()
        self.mock_jump_sound = MockSound()

        self.player = Player(
            pos=(100, 100),
            groups=self.mock_sprites,
            collision_sprites=self.mock_collision_sprites,
            frames=self.mock_frames,
            data=self.mock_data,
            jump_sound=self.mock_jump_sound
        )

    def tearDown(self):
        pygame.quit()

    def test_initial_position(self):
        self.assertEqual(self.player.rect.topleft, (100, 100))

    def test_move_right(self):
        self.player.direction.x = 1
        self.player.move()
        self.assertEqual(self.player.rect.x, 100 + self.player.speed)

    def test_move_left(self):
        self.player.direction.x = -1
        self.player.move()
        self.assertEqual(self.player.rect.x, 100 - self.player.speed)

    def test_gravity_effect(self):
        initial_y = self.player.rect.y
        self.player.jump = True
        self.player.move()
        self.assertEqual(self.player.rect.y, initial_y - self.player.jump_height)

    def test_collision_detection_horizontal(self):
        self.player.rect.x = 0
        self.player.move()
        self.assertEqual(self.player.rect.x, 0)  # The player should not move through the mock sprite

    def test_collision_detection_vertical(self):
        self.player.rect.y = 0
        self.player.direction.y = 1
        self.player.move()
        self.assertEqual(self.player.rect.y, 0)  # The player should not move through the mock sprite

    def test_get_damage(self):
        initial_health = self.mock_data.health
        self.player.get_damage()
        self.assertEqual(self.mock_data.health, initial_health - 1)

    def test_state_idle(self):
        self.player.direction.x = 0
        self.player.get_state()
        self.assertEqual(self.player.state, 'idle')

    def test_state_run(self):
        self.player.direction.x = 1
        self.player.get_state()
        self.assertEqual(self.player.state, 'run')

    def test_flicker(self):
        self.player.get_damage()
        self.player.flicker()
        self.assertTrue(self.player.timers['hit'].active)

    def test_animate(self):
        initial_image = self.player.image
        self.player.animate()
        self.assertNotEqual(self.player.image, initial_image)

    def test_update(self):
        self.player.update()
        self.assertIsNotNone(self.player.rect)

if __name__ == '__main__':
    unittest.main()