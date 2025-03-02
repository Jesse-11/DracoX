import json
import os
import logging



logger = logging.getLogger('bot.config')



class Config:
    """Class to handle bot configuration"""
    


    def __init__(self, config_path='data/config.json'):
  
        self.config_path = config_path
        self._ensure_config_exists()
        self.config = self._load_config()
    




    # Fcuntion to handle config file creation
    def _ensure_config_exists(self):

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
    




    # Function to load configuration from file
    def _load_config(self):

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
    




    # Function to save configuration to file
    def save_config(self):

        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=4)
            logger.info("Configuration saved successfully")
            return True
        except Exception as e:
            logger.error(f"Error saving configuration: {e}")
            return False
    




    #Function to get a configuration value
    def get(self, key, default=None):

        return self.config.get(key, default)
    




    # Function to set a configuration value
    def set(self, key, value):

        self.config[key] = value
        return self.save_config()
    



    #Function to delete a configuration key
    def delete(self, key):
 
        if key in self.config:
            del self.config[key]
            return self.save_config()
        return False
    



    #Function to get all configuration values
    def get_all(self):

        return self.config.copy()