"""
Utility commands for the Discord bot.
"""
import discord
from discord.ext import commands
from sqlalchemy import select
import asyncio

from utils.database import get_db_session
from models.guild import Guild
from utils.helpers import chunk_message

class Utilities(commands.Cog):
    """
    General utility commands.
    """
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def ping(self, ctx):
        """Check the bot's latency."""
        latency = round(self.bot.latency * 1000)
        await ctx.send(f"Pong! Latency: {latency}ms")
    
    @commands.command()
    @commands.guild_only()
    async def serverinfo(self, ctx):
        """Display information about the server."""
        guild = ctx.guild
        
        # Get member counts
        total_members = guild.member_count
        bot_count = sum(1 for member in guild.members if member.bot)
        human_count = total_members - bot_count
        
        # Get channel counts
        text_channels = len(guild.text_channels)
        voice_channels = len(guild.voice_channels)
        categories = len(guild.categories)
        
        # Create embed
        embed = discord.Embed(
            title=f"{guild.name} Info",
            description=guild.description or "No description",
            color=discord.Color.blue()
        )
        
        # Add server icon if available
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        
        # Add fields
        embed.add_field(name="Owner", value=guild.owner.mention, inline=True)
        embed.add_field(name="Server ID", value=guild.id, inline=True)
        embed.add_field(name="Created At", value=guild.created_at.strftime("%Y-%m-%d"), inline=True)
        
        embed.add_field(name="Members", value=f"Total: {total_members}\nHumans: {human_count}\nBots: {bot_count}", inline=True)
        embed.add_field(name="Channels", value=f"Text: {text_channels}\nVoice: {voice_channels}\nCategories: {categories}", inline=True)
        embed.add_field(name="Roles", value=str(len(guild.roles) - 1), inline=True)  # Subtract @everyone
        
        embed.add_field(name="Boost Level", value=f"Level {guild.premium_tier}", inline=True)
        embed.add_field(name="Boost Count", value=guild.premium_subscription_count, inline=True)
        
        await ctx.send(embed=embed)
    
    @commands.command()
    @commands.guild_only()
    async def userinfo(self, ctx, member: discord.Member = None):
        """
        Display information about a user.
        
        Args:
            member: The member to get info for (defaults to command user)
        """
        member = member or ctx.author
        
        # Create embed
        embed = discord.Embed(
            title=f"{member.name} Info",
            color=member.color
        )
        
        # Add user avatar
        if member.avatar:
            embed.set_thumbnail(url=member.avatar.url)
        
        # Add fields
        embed.add_field(name="User ID", value=member.id, inline=True)
        embed.add_field(name="Joined Server", value=member.joined_at.strftime("%Y-%m-%d"), inline=True)
        embed.add_field(name="Account Created", value=member.created_at.strftime("%Y-%m-%d"), inline=True)
        
        roles = [role.mention for role in member.roles if role.name != "@everyone"]
        if roles:
            embed.add_field(name=f"Roles [{len(roles)}]", value=" ".join(roles[:10]) + ("..." if len(roles) > 10 else ""), inline=False)
        
        # Get user's permissions
        if member.guild_permissions.administrator:
            perms = "Administrator (All permissions)"
        else:
            perms = []
            for perm, value in member.guild_permissions:
                if value and perm != "administrator":
                    perms.append(perm.replace("_", " ").title())
            perms = ", ".join(perms[:5]) + ("..." if len(perms) > 5 else "")
        
        embed.add_field(name="Key Permissions", value=perms, inline=False)
        
        await ctx.send(embed=embed)
    
    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def prefix(self, ctx, new_prefix: str = None):
        """
        View or change the server's command prefix.
        
        Args:
            new_prefix: The new prefix to set (leave empty to view current)
        """
        if new_prefix is None:
            # Get current prefix
            async with get_db_session() as session:
                result = await session.execute(
                    select(Guild).where(Guild.guild_id == str(ctx.guild.id))
                )
                guild_config = result.scalars().first()
                
                prefix = guild_config.prefix if guild_config else "!"
                await ctx.send(f"Current prefix is: `{prefix}`")
        else:
            if len(new_prefix) > 5:
                await ctx.send("Prefix cannot be longer than 5 characters.")
                return
            
            # Update prefix
            async with get_db_session() as session:
                result = await session.execute(
                    select(Guild).where(Guild.guild_id == str(ctx.guild.id))
                )
                guild_config = result.scalars().first()
                
                if not guild_config:
                    guild_config = Guild(guild_id=str(ctx.guild.id))
                    session.add(guild_config)
                
                guild_config.prefix = new_prefix
                await session.commit()
                
                await ctx.send(f"Prefix updated to: `{new_prefix}`")
    
    @commands.command()
    async def poll(self, ctx, question: str, *options):
        """
        Create a reaction poll.
        
        Args:
            question: The poll question
            options: Poll options (max 10)
        """
        if len(options) < 2:
            await ctx.send("You need to provide at least 2 options for a poll.")
            return
        
        if len(options) > 10:
            await ctx.send("You can only have up to 10 options in a poll.")
            return
        
        # Emoji options for reactions
        emoji_options = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
        
        # Create the poll message
        description = []
        for i, option in enumerate(options):
            description.append(f"{emoji_options[i]} {option}")
        
        embed = discord.Embed(
            title=question,
            description="\n".join(description),
            color=discord.Color.blue()
        )
        embed.set_footer(text=f"Poll by {ctx.author.name}")
        
        # Send the poll and add reactions
        poll_message = await ctx.send(embed=embed)
        
        for i in range(len(options)):
            await poll_message.add_reaction(emoji_options[i])

async def setup(bot):
    await bot.add_cog(Utilities(bot))