"""
Configuration variables for the Discord bot.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot configuration
PREFIX = os.getenv('COMMAND_PREFIX', '$')
OWNER_IDS = list(map(int, os.getenv('OWNER_IDS', '').split(','))) if os.getenv('OWNER_IDS') else []

# Database configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite+aiosqlite:///bot.db')

# Logging configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_FILE = os.getenv('LOG_FILE', 'bot.log')

# Feature toggles
ENABLE_MODERATION = os.getenv('ENABLE_MODERATION', 'True').lower() in ('true', '1', 't')
ENABLE_ENTERTAINMENT = os.getenv('ENABLE_ENTERTAINMENT', 'True').lower() in ('true', '1', 't')

"""
## Key Takeaways

1. PREFIX: The command prefix users type before commands (default: '$')
   - Allows customization without code changes

2. OWNER_IDS: List of Discord user IDs with admin privileges
    - These users can access special commands and bypass restrictions
    - Stored as a comma-separated string in .env, converted to integers here

3. DATABASE_URL: Connection string for the database
    - Default uses SQLite with aiosqlite for async operations
    - Can be replaced with any SQLAlchemy-compatible connection string
    - Production environments should use a more robust database

4. Logging configuration:
   - LOG_LEVEL: Controls verbosity (DEBUG, INFO, WARNING, ERROR)
   - LOG_FORMAT: Standard timestamp + module + level + message format
   - LOG_FILE: Where logs are stored (useful for debugging issues)

5. Feature toggles:
   - Enable/disable entire modules without code changes
   - ENABLE_MODERATION: Activate moderation commands (kick, ban, etc.)
   - ENABLE_ENTERTAINMENT: Activate entertainment features (games, memes, etc.)
"""