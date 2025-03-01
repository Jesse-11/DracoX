"""
Admin commands for the Discord bot.
Contains server management and moderation commands.
"""
import discord
from discord.ext import commands
import asyncio
from datetime import datetime, timedelta

class AdminCommands(commands.Cog):
    """Commands for server administration and moderation"""
    def __init__(self, bot):
        self.bot = bot
    




    """ Function to clear a specified number of messages """
    @commands.command(name='clear')
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int = 5):
        """Clear a specified number of messages
        
        Args:
            amount: Number of messages to delete (default: 5)
        """
        if amount > 100:
            await ctx.send("You can only delete up to 100 messages at once.")
            return
            
        await ctx.channel.purge(limit=amount + 1)  # +1 to include command
        confirmation = await ctx.send(f'Cleared {amount} messages.')
        await asyncio.sleep(5)
        await confirmation.delete()
    




    """ Function to kick a member from the server """
    @commands.command(name='kick')
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        """Kick a member from the server
        
        Args:
            member: The member to kick (mention or ID)
            reason: Reason for kicking (optional)
        """
        await member.kick(reason=reason)
        await ctx.send(f'{member.mention} has been kicked. Reason: {reason or "No reason provided"}')
    




    """ Function to ban a member from the server """
    @commands.command(name='ban')
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        """Ban a member from the server
        
        Args:
            member: The member to ban (mention or ID)
            reason: Reason for banning (optional)
        """
        await member.ban(reason=reason)
        await ctx.send(f'{member.mention} has been banned. Reason: {reason or "No reason provided"}')
    




    """ Function to timeout a member for a specified duration """	
    @commands.command(name='timeout')
    @commands.has_permissions(moderate_members=True)
    async def timeout(self, ctx, member: discord.Member, minutes: int, *, reason=None):
        """Timeout a member for a specified duration
        
        Args:
            member: The member to timeout (mention or ID)
            minutes: Duration of timeout in minutes
            reason: Reason for timeout (optional)
        """
        if minutes > 40320:  # Max 28 days
            await ctx.send("Timeout cannot exceed 28 days (40320 minutes)")
            return
            
        until = datetime.now() + timedelta(minutes=minutes)
        await member.timeout(until, reason=reason)
        await ctx.send(f'{member.mention} has been timed out for {minutes} minutes. Reason: {reason or "No reason provided"}')
    





    """ Function to setup basic welcome and log channels for the server """	
    @commands.command(name='setup')
    @commands.has_permissions(administrator=True)
    async def setup(self, ctx):
        """Setup basic channels and roles for the server"""
        from utils.config import Config
        config = Config()
        
        # Create welcome channel if it doesn't exist
        if not config.get('welcome_channel'):
            welcome_channel = await ctx.guild.create_text_channel('welcome')
            config.set('welcome_channel', welcome_channel.id)
            await ctx.send(f"Created welcome channel: {welcome_channel.mention}")
        
        # Create log channel if it doesn't exist
        if not config.get('log_channel'):
            log_channel = await ctx.guild.create_text_channel('bot-logs')
            config.set('log_channel', log_channel.id)
            await ctx.send(f"Created log channel: {log_channel.mention}")
            
        await ctx.send("Setup complete!")
    





    """------------------------------ Error Handlers ------------------------------"""

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to use this command.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Please provide a valid number of messages to delete.")
    

    @kick.error
    @ban.error
    @timeout.error
    async def mod_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to use this command.")
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send("Member not found. Please provide a valid mention or ID.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Please provide valid arguments for the command.")







""" Function to add the cog to the bot """	
async def setup(bot):
    """Add the cog to the bot"""
    await bot.add_cog(AdminCommands(bot))