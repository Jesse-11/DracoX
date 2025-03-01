"""
Helper functions for common tasks.
"""
import discord
import re
import logging
from datetime import datetime, timedelta

logger = logging.getLogger('bot.helpers')

def format_time(seconds):
    """Format seconds into a human-readable time string
    
    Args:
        seconds: Number of seconds
        
    Returns:
        Formatted time string (e.g. "3:45" or "1:23:45")
    """
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    
    if hours > 0:
        return f"{int(hours)}:{int(minutes):02d}:{int(seconds):02d}"
    else:
        return f"{int(minutes)}:{int(seconds):02d}"

def get_thumbnail(url):
    """Extract YouTube thumbnail URL from video URL
    
    Args:
        url: YouTube video URL
        
    Returns:
        Thumbnail URL or None if not a valid YouTube URL
    """
    # Extract video ID from various YouTube URL formats
    patterns = [
        r'youtube\.com/watch\?v=([a-zA-Z0-9_-]+)',
        r'youtu\.be/([a-zA-Z0-9_-]+)',
        r'youtube\.com/embed/([a-zA-Z0-9_-]+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            video_id = match.group(1)
            return f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
    
    return None

def parse_time(time_str):
    """Parse a time string into seconds
    
    Args:
        time_str: Time string (e.g. "3:45" or "1:23:45")
        
    Returns:
        Number of seconds or None if invalid format
    """
    parts = time_str.split(':')
    try:
        if len(parts) == 2:  # MM:SS
            minutes, seconds = parts
            return int(minutes) * 60 + int(seconds)
        elif len(parts) == 3:  # HH:MM:SS
            hours, minutes, seconds = parts
            return int(hours) * 3600 + int(minutes) * 60 + int(seconds)
        else:
            return None
    except ValueError:
        return None

def is_url(string):
    """Check if a string is a URL
    
    Args:
        string: String to check
        
    Returns:
        True if the string is a URL, False otherwise
    """
    url_pattern = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain
        r'localhost|'  # localhost
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # or IP
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        
    return bool(url_pattern.match(string))

def create_embed(title, description=None, color=discord.Color.blue(), fields=None, footer=None, thumbnail=None):
    """Create a Discord embed with common formatting
    
    Args:
        title: Embed title
        description: Embed description
        color: Embed color
        fields: List of dicts with name, value, inline keys
        footer: Footer text
        thumbnail: Thumbnail URL
        
    Returns:
        discord.Embed object
    """
    embed = discord.Embed(
        title=title,
        description=description,
        color=color,
        timestamp=datetime.now()
    )
    
    if fields:
        for field in fields:
            embed.add_field(
                name=field['name'],
                value=field['value'],
                inline=field.get('inline', False)
            )
    
    if footer:
        embed.set_footer(text=footer)
    
    if thumbnail:
        embed.set_thumbnail(url=thumbnail)
    
    return embed

def log_to_channel(bot, guild_id, message, level="INFO"):
    """Log a message to the guild's log channel
    
    Args:
        bot: Bot instance
        guild_id: Guild ID
        message: Message to log
        level: Log level
        
    Returns:
        True if logged successfully, False otherwise
    """
    from utils.config import Config
    config = Config()
    
    log_channel_id = config.get('log_channel')
    if not log_channel_id:
        return False
    
    log_channel = bot.get_channel(log_channel_id)
    if not log_channel:
        return False
    
    # Create color based on level
    color_map = {
        "INFO": discord.Color.blue(),
        "WARNING": discord.Color.gold(),
        "ERROR": discord.Color.red(),
        "SUCCESS": discord.Color.green()
    }
    color = color_map.get(level.upper(), discord.Color.default())
    
    embed = create_embed(
        title=f"{level.upper()} Log",
        description=message,
        color=color,
        footer=f"Guild ID: {guild_id}"
    )
    
    try:
        bot.loop.create_task(log_channel.send(embed=embed))
        return True
    except Exception as e:
        logger.error(f"Error logging to channel: {e}")
        return False