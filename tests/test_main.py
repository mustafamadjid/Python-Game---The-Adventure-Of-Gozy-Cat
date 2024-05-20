import unittest
from unittest.mock import patch, MagicMock
from src.main import GozyGame

class TestGozyGame(unittest.TestCase):

    @patch('pygame.mixer.music.load')
    @patch('pygame.mixer.music.set_volume')
    @patch('pygame.mixer.music.play')
    def test_change_music(self, mock_play, mock_set_volume, mock_load):
        game = GozyGame()
        game.change_music("test_music.ogg")

        mock_load.assert_called_once_with('../Assets/Sound/Music Background/test_music.ogg')
        mock_set_volume.assert_called_once_with(0.5)
        mock_play.assert_called_once_with(-1)

    @patch('Src.main.Level')  # Mock the Level class
    @patch('Src.main.Overworld')  # Mock the Overworld class
    def test_switch_stage(self, MockOverworld, MockLevel):
        game = GozyGame()
        game.data = MagicMock()  # Mock the data attribute

        # Test switching to level
        game.switch_stage('level')
        MockLevel.assert_called_once()
        MockOverworld.assert_not_called()

        # Test switching to overworld with unlock
        game.switch_stage('overworld', unlock=1)
        game.data.unlocked_level = 1
        MockOverworld.assert_called_once()
        self.assertEqual(game.data.unlocked_level, 1)

        # Test switching to overworld without unlock
        game.switch_stage('overworld', unlock=0)
        game.data.health -= 1
        self.assertEqual(game.data.health, -1)

    @patch('Src.main.import_folder')
    @patch('Src.main.import_image')
    @patch('Src.main.import_sub_folders')
    @patch('pygame.font.Font')
    def test_import_assets(self, mock_font, mock_import_sub_folders, mock_import_image, mock_import_folder):
        game = GozyGame()
        game.import_assets()

        self.assertTrue(mock_import_folder.called)
        self.assertTrue(mock_import_image.called)
        self.assertTrue(mock_import_sub_folders.called)
        mock_font.assert_called_once_with('../Assets/ui/runescape_uf.ttf', 40)

if __name__ == '__main__':
    unittest.main()
