"""
General commands for the Discord bot.
Contains utility and informational commands.
"""
import discord
from discord.ext import commands
import platform
import time
from datetime import datetime

class General(commands.Cog):
    """General purpose commands"""
    
    def __init__(self, bot):
        self.bot = bot
        self.start_time = datetime.now()
    
    @commands.command(name='ping')
    async def ping(self, ctx):
        """Check the bot's latency"""
        start_time = time.time()
        message = await ctx.send("Pinging...")
        end_time = time.time()
        
        api_latency = round(self.bot.latency * 1000)
        response_time = round((end_time - start_time) * 1000)
        
        embed = discord.Embed(title="Pong!", color=discord.Color.green())
        embed.add_field(name="API Latency", value=f"{api_latency}ms", inline=True)
        embed.add_field(name="Response Time", value=f"{response_time}ms", inline=True)
        
        await message.edit(content=None, embed=embed)
    
    @commands.command(name='info')
    async def info(self, ctx):
        """Display information about the bot"""
        embed = discord.Embed(
            title=f"{self.bot.user.name} Info",
            description="A modular Discord bot built with discord.py",
            color=discord.Color.blue(),
            timestamp=datetime.now()
        )
        
        # Bot information
        embed.add_field(name="Bot Version", value="1.0.0", inline=True)
        embed.add_field(name="discord.py Version", value=discord.__version__, inline=True)
        embed.add_field(name="Python Version", value=platform.python_version(), inline=True)
        
        # Statistics
        uptime = datetime.now() - self.start_time
        days, remainder = divmod(int(uptime.total_seconds()), 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        embed.add_field(
            name="Uptime", 
            value=f"{days}d {hours}h {minutes}m {seconds}s", 
            inline=True
        )
        embed.add_field(name="Servers", value=str(len(self.bot.guilds)), inline=True)
        embed.add_field(name="Commands", value=str(len(self.bot.commands)), inline=True)
        
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
        embed.set_thumbnail(url=self.bot.user.avatar.url if self.bot.user.avatar else None)
        
        await ctx.send(embed=embed)
    
    @commands.command(name='help')
    async def help_command(self, ctx, command=None):
        """Show help for commands
        
        Args:
            command: Specific command to get help for (optional)
        """
        prefix = '!'  # Get from config in a real bot
        
        if command:
            # Help for specific command
            cmd = self.bot.get_command(command)
            if not cmd:
                await ctx.send(f"Command `{command}` not found.")
                return
                
            embed = discord.Embed(
                title=f"Help: {prefix}{cmd.name}",
                description=cmd.help or "No description available.",
                color=discord.Color.blue()
            )
            
            if cmd.aliases:
                embed.add_field(name="Aliases", value=", ".join(cmd.aliases), inline=False)
                
            usage = f"{prefix}{cmd.name}"
            if cmd.signature:
                usage += f" {cmd.signature}"
            embed.add_field(name="Usage", value=f"`{usage}`", inline=False)
            
            await ctx.send(embed=embed)
            return
        
        # General help
        embed = discord.Embed(
            title="Bot Commands",
            description=f"Use `{prefix}help <command>` for more info on a command.",
            color=discord.Color.blue()
        )
        
        # Group commands by cog
        for cog_name, cog in self.bot.cogs.items():
            commands_list = cog.get_commands()
            if not commands_list:
                continue
                
            command_names = [f"`{prefix}{cmd.name}`" for cmd in commands_list if not cmd.hidden]
            if command_names:
                embed.add_field(
                    name=cog_name,
                    value=", ".join(command_names),
                    inline=False
                )
        
        await ctx.send(embed=embed)
    
    @commands.command(name='serverinfo')
    async def server_info(self, ctx):
        """Display information about the current server"""
        guild = ctx.guild
        
        # Get role count excluding @everyone
        role_count = len(guild.roles) - 1
        
        # Get channel counts
        text_channels = len(guild.text_channels)
        voice_channels = len(guild.voice_channels)
        categories = len(guild.categories)
        
        # Create embed
        embed = discord.Embed(
            title=f"{guild.name} Info",
            description=guild.description or "No description",
            color=discord.Color.gold(),
            timestamp=datetime.now()
        )
        
        # Server information
        embed.add_field(name="Owner", value=guild.owner.mention, inline=True)
        embed.add_field(name="Created", value=guild.created_at.strftime("%Y-%m-%d"), inline=True)
        embed.add_field(name="Region", value=str(guild.region) if hasattr(guild, 'region') else "N/A", inline=True)
        
        # Statistics
        embed.add_field(name="Members", value=guild.member_count, inline=True)
        embed.add_field(name="Roles", value=role_count, inline=True)
        embed.add_field(name="Emojis", value=len(guild.emojis), inline=True)
        embed.add_field(name="Text Channels", value=text_channels, inline=True)
        embed.add_field(name="Voice Channels", value=voice_channels, inline=True)
        embed.add_field(name="Categories", value=categories, inline=True)
        
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        
        await ctx.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Send welcome message when a new member joins"""
        from utils.config import Config
        config = Config()
        
        welcome_channel_id = config.get('welcome_channel')
        if welcome_channel_id:
            channel = self.bot.get_channel(welcome_channel_id)
            if channel:
                embed = discord.Embed(
                    title=f"Welcome to {member.guild.name}!",
                    description=f"Hello {member.mention}! Welcome to the server!",
                    color=discord.Color.green()
                )
                embed.set_thumbnail(url=member.avatar.url if member.avatar else None)
                await channel.send(embed=embed)

async def setup(bot):
    """Add the cog to the bot"""
    await bot.add_cog(General(bot))