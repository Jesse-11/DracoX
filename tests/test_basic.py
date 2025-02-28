"""
Basic tests for the Discord bot.
"""
import unittest
from unittest.mock import AsyncMock, patch

class TestBasicFunctionality(unittest.TestCase):
    """
    Tests for basic bot functionality.
    """
    
    def test_config_loading(self):
        """Test that config values can be loaded."""
        with patch('os.getenv') as mock_getenv:
            mock_getenv.return_value = 'test_token'
            
            import config
            from importlib import reload
            reload(config)
            
            self.assertEqual(config.PREFIX, '!')
    
    @patch('discord.ext.commands.Bot')
    def test_bot_initialization(self, mock_bot):
        """Test that the bot can be initialized."""
        with patch('os.getenv') as mock_getenv:
            mock_getenv.return_value = 'test_token'
            
            from main import DiscordBot
            
            bot = DiscordBot()
            self.assertIsNotNone(bot)

if __name__ == '__main__':
    unittest.main()