import discord
import re
import logging
from datetime import datetime, timedelta


logger = logging.getLogger('bot.helpers')




# Function to format time
def format_time(seconds):

    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    
    if hours > 0:
        return f"{int(hours)}:{int(minutes):02d}:{int(seconds):02d}"
    else:
        return f"{int(minutes)}:{int(seconds):02d}"








# Function to parse time
def parse_time(time_str):

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










# Function to create an embed
def create_embed(title, description=None, color=discord.Color.blue(), fields=None, footer=None, thumbnail=None):

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





# Function to log to channel
def log_to_channel(bot, guild_id, message, level="INFO"):

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