"""
Bot client setup and configuration.
Contains the main bot class and setup logic.
"""
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('bot')

# Load environment variables
load_dotenv()
TOKEN = os.getenv('TOKEN')

# Define intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

class DiscordBot:
    """
    Main bot class responsible for setting up and running the Discord bot.
    """
    def __init__(self):
        self.bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)
        
        @self.bot.event
        async def on_ready():
            """Called when the bot is ready and connected to Discord"""
            await self.bot.change_presence(
                activity=discord.Activity(
                    type=discord.ActivityType.listening, 
                    name="commands | !help"
                )
            )
            logger.info(f'{self.bot.user.name} has connected to Discord!')
        
        # Set up the async setup hook
        self.bot.setup_hook = self.setup_hook
    
    async def setup_hook(self):
        """Async setup hook called before the bot starts running"""
        await self._load_cogs()
    
    async def _load_cogs(self):
        """Load all command cogs from the cogs directory"""
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py') and not filename.startswith('__'):
                try:
                    await self.bot.load_extension(f'cogs.{filename[:-3]}')
                    logger.info(f'Loaded extension: {filename[:-3]}')
                except Exception as e:
                    logger.error(f'Failed to load extension {filename[:-3]}: {e}')
    
    def run_bot(self):
        """Start the bot"""
        try:
            logger.info("Starting bot...")
            self.bot.run(TOKEN)
        except Exception as e:
            logger.critical(f"Failed to start bot: {e}")

# Create bot instance
bot = DiscordBot()