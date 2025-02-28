"""
Main entry point for bot
"""

import discord
import os
from dotenv import load_dotenv
from discord.ext import commands

from utils.logger import setup_logger
from utils.database import init_db

#load the environment variables
load_dotenv()
token  = os.getenv('TOKEN')
if token is None:
    raise ValueError("TOKEN environment variable is not set or .env file not found")


#setup the logger
logger = setup_logger('bot')


#bot config
intents = discord.Intents.default()
intents.members = True
intents.message_content = True



class DiscordBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix='$',
            intents=intents,
            help_command= commands.DefaultHelpCommand(),
            description="Bot description placeholder"
        )
        self.logger = logger

    async def setup_hook(self):

        #initialize the database
        await init_db()

        #load cogs
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py') and not filename.startswith('_'):
                try:
                    await self.load_extension(f'cogs.{filename[:-3]}')
                    self.logger.info(f'Loaded extension {filename[:-3]}')
                except Exception as e:
                    self.logger.error(f'Failed to load extension {filename}: {e}')

    async def on_ready(self):
        self.logger.info(f'Logged in as {self.user.name} ({self.user.id})')
        await self.change_presence(activity=discord.Game(name="$help for commands"))

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("Command not found. Use $help to see available commands")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Missing required argument: {error}")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have permission to run this command")
        else:
            self.logger.error(f'Error in command {ctx.command}: {error}')
            await ctx.send("An error occurred while processing the command")

# Bot initialization and run
bot = DiscordBot()

if __name__ == '__main__':
    bot.run(token, log_handler=None)  # Using custom logger