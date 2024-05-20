import unittest
from unittest.mock import patch, MagicMock, call
import pygame
from src.level import Level
from src.data import Data
from src.settings import *

class TestLevel(unittest.TestCase):
    def setUp(self):
        # Mock tmx_map
        self.tmx_map_mock = MagicMock()
        self.tmx_map_mock.width = 100
        self.tmx_map_mock.height = 50
        self.tmx_map_mock.get_layer_by_name.return_value = [MagicMock(properties={'level_unlock': 1})]

        # Mock frames and audio files
        self.level_frames = {
            'Particle': MagicMock(),
            'Hit': MagicMock(),
            'player': MagicMock(),
            'Slime_2': MagicMock(),
            'Slime_3': MagicMock(),
            'Skeleton': MagicMock(),
            'House': MagicMock(),
            'Fish': MagicMock(),
            'Chicken': MagicMock(),
            'Food': MagicMock(),
        }
        self.audio_files = {
            'snack': MagicMock(),
            'jump': MagicMock(),
        }

        # Mock Data
        self.data_mock = MagicMock()

        # Mock switch_stage method
        self.switch_stage_mock = MagicMock()

        # Instantiate Level
        self.level = Level(self.tmx_map_mock, self.level_frames, self.audio_files, self.data_mock, self.switch_stage_mock)

    @patch('level.pygame.display.get_surface', return_value=MagicMock())
    def test_initialization(self, mock_get_surface):
        self.assertEqual(self.level.level_width, self.tmx_map_mock.width * TILE_SIZE)
        self.assertEqual(self.level.level_bottom, self.tmx_map_mock.height * TILE_SIZE)
        self.assertEqual(self.level.level_unlock, 1)
        self.assertIsNotNone(self.level.display_surface)

    @patch('level.pygame.sprite.Sprite')
    def test_setup(self, mock_sprite):
        # Run setup
        self.level.setup(self.tmx_map_mock, self.level_frames, self.audio_files)
        
        # Check if sprites are created
        self.assertTrue(mock_sprite.called)

    def test_check_constraint(self):
        # Mock player rect
        self.level.player = MagicMock()
        self.level.player.rect = MagicMock()
        self.level.player.rect.left = -10
        self.level.player.rect.right = self.level.level_width + 10
        self.level.player.rect.bottom = self.level.level_bottom + 10

        # Run check_constraint
        self.level.check_constraint()

        # Assertions
        self.assertEqual(self.level.player.rect.left, 0)
        self.assertEqual(self.level.player.rect.right, self.level.level_width)
        self.switch_stage_mock.assert_called_with('overworld', -1)

    def test_hit_collision(self):
        # Mock player and damage sprites
        self.level.player = MagicMock()
        self.level.player.rect = MagicMock()
        damage_sprite_mock = MagicMock()
        damage_sprite_mock.rect.colliderect.return_value = True
        self.level.damage_sprites.add(damage_sprite_mock)

        # Run hit_collision
        self.level.hit_collision()

        # Assertions
        self.level.player.get_damage.assert_called()

    def test_item_collision(self):
        # Mock player and item sprites
        self.level.player = MagicMock()
        self.level.player.rect = MagicMock()
        item_sprite_mock = MagicMock()
        item_sprite_mock.rect.colliderect.return_value = True
        self.level.item_sprites.add(item_sprite_mock)

        # Run item_collision
        self.level.item_collision()

        # Assertions
        self.assertTrue(self.audio_files['snack'].play.called)
        self.assertTrue(item_sprite_mock.activate.called)

    @patch('level.pygame.display.get_surface', return_value=MagicMock())
    @patch('level.pygame.sprite.spritecollide', return_value=[MagicMock()])
    def test_run(self, mock_spritecollide, mock_get_surface):
        # Mock methods
        self.level.check_constraint = MagicMock()
        self.level.hit_collision = MagicMock()
        self.level.item_collision = MagicMock()

        # Run run method
        self.level.run()

        # Assertions
        self.level.check_constraint.assert_called()
        self.level.hit_collision.assert_called()
        self.level.item_collision.assert_called()

if __name__ == "__main__":
    unittest.main()
