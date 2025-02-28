"""
Event handlers for the Discord bot.
"""
import discord
from discord.ext import commands
from sqlalchemy import select

from utils.database import get_db_session
from models.guild import Guild

class Events(commands.Cog):
    """
    Event handlers for various Discord events.
    """
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        """
        Called when the bot joins a new guild.
        
        Args:
            guild: The guild that was joined
        """
        self.bot.logger.info(f"Joined new guild: {guild.name} (ID: {guild.id})")
        
        # Create guild config in database
        async with get_db_session() as session:
            # Check if guild already exists in database
            result = await session.execute(
                select(Guild).where(Guild.guild_id == str(guild.id))
            )
            guild_config = result.scalars().first()
            
            if not guild_config:
                guild_config = Guild(guild_id=str(guild.id))
                session.add(guild_config)
                await session.commit()
                self.bot.logger.info(f"Created new guild config for {guild.name}")
    
    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        """
        Called when the bot is removed from a guild.
        
        Args:
            guild: The guild that was left
        """
        self.bot.logger.info(f"Left guild: {guild.name} (ID: {guild.id})")
        
        # You could choose to remove guild data here, or keep it for if the bot rejoins
        # For this example, we'll keep the data
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        """
        Called when a member joins a guild.
        
        Args:
            member: The member who joined
        """
        guild = member.guild
        self.bot.logger.info(f"Member {member.name} (ID: {member.id}) joined guild: {guild.name}")
        
        # Check if welcome messages are enabled for this guild
        async with get_db_session() as session:
            result = await session.execute(
                select(Guild).where(Guild.guild_id == str(guild.id))
            )
            guild_config = result.scalars().first()
            
            if guild_config and guild_config.welcome_enabled and guild_config.welcome_channel_id:
                channel = guild.get_channel(int(guild_config.welcome_channel_id))
                if channel:
                    # Replace placeholders in welcome message
                    message = guild_config.welcome_message or f"Welcome to {guild.name}, {member.mention}!"
                    message = message.replace("{user}", member.mention)
                    message = message.replace("{server}", guild.name)
                    message = message.replace("{count}", str(guild.member_count))
                    
                    await channel.send(message)
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """
        Global error handler for command errors.
        
        Args:
            ctx: The context in which the command was invoked
            error: The error that was raised
        """
        # This is a backup error handler in case the one in the bot class doesn't catch it
        if hasattr(ctx.command, 'on_error'):
            # If the command has its own error handler, don't do anything
            return
        
        # Get the original error if it's wrapped in a CommandInvokeError
        error = getattr(error, 'original', error)
        
        if isinstance(error, commands.CommandNotFound):
            # Ignore command not found errors
            return
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Missing required argument: {error.param.name}")
        elif isinstance(error, commands.BadArgument):
            await ctx.send(f"Bad argument: {error}")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to use this command.")
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send(f"I don't have the required permissions to do this.")
        else:
            # Log unexpected errors
            self.bot.logger.error(f"Unhandled error in command {ctx.command}: {error}")

async def setup(bot):
    await bot.add_cog(Events(bot))