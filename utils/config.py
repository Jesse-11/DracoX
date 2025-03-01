"""
Configuration management utilities.
Handles loading and saving configuration data.
"""
import json
import os
import logging

logger = logging.getLogger('bot.config')

class Config:
    """Class to handle bot configuration"""
    
    def __init__(self, config_path='data/config.json'):
        """Initialize configuration
        
        Args:
            config_path: Path to the config file
        """
        self.config_path = config_path
        self._ensure_config_exists()
        self.config = self._load_config()
    




    """ Fcuntion to handle config file creation"""
    def _ensure_config_exists(self):
        """Create config file if it doesn't exist"""
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        if not os.path.exists(self.config_path):
            logger.info(f"Creating new configuration file at {self.config_path}")
            with open(self.config_path, 'w') as f:
                json.dump({
                    "prefix": "!",
                    "welcome_channel": None,
                    "log_channel": None,
                    "custom_commands": {}
                }, f, indent=4)
    




    """ Function to load configuration from file"""
    def _load_config(self):
        """Load configuration from file"""
        try:
            with open(self.config_path, 'r') as f:
                config = json.load(f)
                logger.info("Configuration loaded successfully")
                return config
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            # Return default config if loading fails
            return {
                "prefix": "!",
                "welcome_channel": None,
                "log_channel": None,
                "custom_commands": {}
            }
    




    """ Function to save configuration to file"""
    def save_config(self):
        """Save configuration to file"""
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=4)
            logger.info("Configuration saved successfully")
            return True
        except Exception as e:
            logger.error(f"Error saving configuration: {e}")
            return False
    




    """ Function to get a configuration value"""
    def get(self, key, default=None):
        """Get a configuration value
        
        Args:
            key: The configuration key to retrieve
            default: Default value if key doesn't exist
            
        Returns:
            The configuration value or default value
        """
        return self.config.get(key, default)
    




    """ Function to set a configuration value"""	
    def set(self, key, value):
        """Set a configuration value
        
        Args:
            key: The configuration key to set
            value: The value to set
            
        Returns:
            True if saved successfully, False otherwise
        """
        self.config[key] = value
        return self.save_config()
    



    """ Function to delete a configuration key"""
    def delete(self, key):
        """Delete a configuration key
        
        Args:
            key: The configuration key to delete
            
        Returns:
            True if key was deleted and saved successfully, False otherwise
        """
        if key in self.config:
            del self.config[key]
            return self.save_config()
        return False
    




    """ Function to get all configuration values"""
    def get_all(self):
        """Get all configuration values
        
        Returns:
            Dictionary of all configuration values
        """
        return self.config.copy()