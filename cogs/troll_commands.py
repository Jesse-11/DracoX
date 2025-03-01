import discord
from discord.ext import commands
import random
import asyncio
import datetime

class TrollCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.typing_tasks = {}  # For tracking endless typing indicators
    
    
    @commands.command(name='ghostping')
    async def ghost_ping(self, ctx, target: discord.Member = None):
        """Ghost ping a user - ping them and then delete the message"""
        if target is None:
            await ctx.send("Please mention a user to ghost ping")
            return
            
        # Send a message mentioning the user
        message = await ctx.send(f"{target.mention}")
        
        # Delete both the command and the ping immediately
        await ctx.message.delete()
        await message.delete()
    
    @commands.command(name='impersonate')
    @commands.has_permissions(manage_webhooks=True)
    async def impersonate(self, ctx, target: discord.Member, *, message=None):
        """Send a message as if it's from someone else (needs webhook permissions)"""
        if message is None:
            await ctx.send("Please provide a message to send")
            return
            
        # Delete the command message
        await ctx.message.delete()
        
        # Create a webhook
        webhook = await ctx.channel.create_webhook(name=target.display_name)
        
        try:
            # Send the message with the target's username and avatar
            await webhook.send(
                content=message,
                username=target.display_name,
                avatar_url=target.display_avatar.url
            )
        finally:
            # Clean up the webhook afterward
            await webhook.delete()
    
    @commands.command(name='disconnect')
    @commands.has_permissions(move_members=True)
    async def disconnect_user(self, ctx, target: discord.Member = None):
        """Disconnect a user from voice channel"""
        if target is None:
            await ctx.send("Please mention a user to disconnect")
            return
            
        if target.voice is None:
            await ctx.send(f"{target.mention} is not in a voice channel")
            return
            
        await target.move_to(None)  # Disconnect the user
        await ctx.message.delete()  # Delete the command for stealth
    
    
    
async def setup(bot):
    await bot.add_cog(TrollCommands(bot))