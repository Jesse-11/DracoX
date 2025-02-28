"""
Moderation commands for the Discord bot.
"""
import discord
from discord.ext import commands
import asyncio
from datetime import datetime, timedelta

from utils.database import get_db_session
from utils.helpers import parse_time, format_timedelta
from models.infraction import Infraction

class Moderation(commands.Cog):
    """
    Commands for server moderation.
    """
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def warn(self, ctx, member: discord.Member, *, reason: str = "No reason provided"):
        """
        Warn a user.
        
        Args:
            member: The member to warn
            reason: The reason for the warning
        """
        if member.top_role >= ctx.author.top_role and ctx.author.id != ctx.guild.owner_id:
            await ctx.send("You cannot warn someone with a higher or equal role.")
            return
        
        # Create infraction record
        async with get_db_session() as session:
            infraction = Infraction(
                user_id=str(member.id),
                guild_id=str(ctx.guild.id),
                moderator_id=str(ctx.author.id),
                type="warning",
                reason=reason,
                timestamp=datetime.utcnow()
            )
            session.add(infraction)
            await session.commit()
            
        # Notify user
        try:
            await member.send(f"You have been warned in {ctx.guild.name} for: {reason}")
        except discord.HTTPException:
            await ctx.send(f"Could not DM user about the warning.")
            
        await ctx.send(f"User {member.mention} has been warned. Reason: {reason}")
        self.bot.logger.info(f"User {member.id} warned in guild {ctx.guild.id} by {ctx.author.id}")
    
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def mute(self, ctx, member: discord.Member, duration: str, *, reason: str = "No reason provided"):
        """
        Mute a user for a specified duration.
        
        Args:
            member: The member to mute
            duration: Duration in format like 1h, 30m, 1d
            reason: The reason for the mute
        """
        if member.top_role >= ctx.author.top_role and ctx.author.id != ctx.guild.owner_id:
            await ctx.send("You cannot mute someone with a higher or equal role.")
            return
        
        # Parse duration
        try:
            seconds = parse_time(duration)
        except ValueError:
            await ctx.send("Invalid duration format. Use s, m, h, d, or w (e.g., 30m, 1h, 1d)")
            return
        
        # Get or create mute role
        mute_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not mute_role:
            mute_role = await ctx.guild.create_role(name="Muted")
            
            # Set permissions for mute role
            for channel in ctx.guild.channels:
                await channel.set_permissions(mute_role, speak=False, send_messages=False, add_reactions=False)
        
        # Apply mute
        await member.add_roles(mute_role)
        
        # Log infraction
        async with get_db_session() as session:
            infraction = Infraction(
                user_id=str(member.id),
                guild_id=str(ctx.guild.id),
                moderator_id=str(ctx.author.id),
                type="mute",
                reason=reason,
                timestamp=datetime.utcnow(),
                expires_at=datetime.utcnow() + timedelta(seconds=seconds)
            )
            session.add(infraction)
            await session.commit()
            
        # Notify user and channel
        expiry_time = format_timedelta(timedelta(seconds=seconds))
        await ctx.send(f"{member.mention} has been muted for {expiry_time}. Reason: {reason}")
        
        # Schedule unmute
        await asyncio.sleep(seconds)
        
        # Check if the user still has the role (they might have been manually unmuted)
        if member in ctx.guild.members and mute_role in member.roles:
            await member.remove_roles(mute_role)
            await ctx.send(f"{member.mention} has been automatically unmuted.")
    
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def unmute(self, ctx, member: discord.Member):
        """
        Unmute a muted user.
        
        Args:
            member: The member to unmute
        """
        mute_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not mute_role:
            await ctx.send("No mute role found.")
            return
        
        if mute_role not in member.roles:
            await ctx.send(f"{member.mention} is not muted.")
            return
        
        await member.remove_roles(mute_role)
        await ctx.send(f"{member.mention} has been unmuted.")
    
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason: str = "No reason provided"):
        """
        Kick a user from the server.
        
        Args:
            member: The member to kick
            reason: The reason for the kick
        """
        if member.top_role >= ctx.author.top_role and ctx.author.id != ctx.guild.owner_id:
            await ctx.send("You cannot kick someone with a higher or equal role.")
            return
        
        # Log infraction
        async with get_db_session() as session:
            infraction = Infraction(
                user_id=str(member.id),
                guild_id=str(ctx.guild.id),
                moderator_id=str(ctx.author.id),
                type="kick",
                reason=reason,
                timestamp=datetime.utcnow()
            )
            session.add(infraction)
            await session.commit()
        
        # Notify user
        try:
            await member.send(f"You have been kicked from {ctx.guild.name} for: {reason}")
        except discord.HTTPException:
            pass
        
        # Kick user
        await member.kick(reason=reason)
        await ctx.send(f"{member.name} has been kicked. Reason: {reason}")

async def setup(bot):
    await bot.add_cog(Moderation(bot))