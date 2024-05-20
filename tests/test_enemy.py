import unittest
import pygame
from random import choice
from src.enemy import Enemy

# Mock classes
class MockSprite(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.rect = pygame.Rect(pos, (50, 50))
        self.old_rect = self.rect.copy()

# Unit tests
class TestEnemy(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.mock_sprites = pygame.sprite.Group()
        self.mock_collision_sprites = pygame.sprite.Group(MockSprite((0, 0)))
        self.mock_frames = [pygame.Surface((50, 50)) for _ in range(3)]

        self.enemy = Enemy(
            pos=(100, 100),
            frames=self.mock_frames,
            groups=self.mock_sprites,
            collision_sprites=self.mock_collision_sprites
        )

    def tearDown(self):
        pygame.quit()

    def test_initial_position(self):
        self.assertEqual(self.enemy.rect.topleft, (100, 100))

    def test_initial_direction(self):
        self.assertIn(self.enemy.direction, (-1, 1))

    def test_initial_speed(self):
        self.assertEqual(self.enemy.speed, 1)

    def test_animation(self):
        initial_image = self.enemy.image
        self.enemy.update()
        self.assertNotEqual(self.enemy.image, initial_image)

    def test_move(self):
        initial_x = self.enemy.rect.x
        self.enemy.update()
        self.assertNotEqual(self.enemy.rect.x, initial_x)

    def test_reverse_direction_right(self):
        self.enemy.direction = 1
        self.enemy.rect.x = 200
        self.enemy.update()
        self.assertEqual(self.enemy.direction, -1)

    def test_reverse_direction_left(self):
        self.enemy.direction = -1
        self.enemy.rect.x = 0
        self.enemy.update()
        self.assertEqual(self.enemy.direction, 1)

if __name__ == '__main__':
    unittest.main()
