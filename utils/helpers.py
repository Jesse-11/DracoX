"""
Helper functions for the Discord bot.
"""
import re
from datetime import timedelta

def parse_time(time_str):
    """
    Parse a time string into seconds.
    
    Args:
        time_str (str): Time string (e.g., "1d", "2h", "30m", "10s")
        
    Returns:
        int: Time in seconds
        
    Raises:
        ValueError: If the time string is invalid
    """
    time_units = {
        's': 1,
        'm': 60,
        'h': 3600,
        'd': 86400,
        'w': 604800
    }
    
    match = re.match(r'^(\d+)([smhdw])$', time_str.lower())
    if not match:
        raise ValueError(f"Invalid time format: {time_str}")
    
    amount, unit = match.groups()
    return int(amount) * time_units[unit]

def format_timedelta(td):
    """
    Format a timedelta into a human-readable string.
    
    Args:
        td (timedelta): Timedelta object
        
    Returns:
        str: Formatted string
    """
    seconds = int(td.total_seconds())
    
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    
    parts = []
    if days > 0:
        parts.append(f"{days}d")
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if seconds > 0 or not parts:
        parts.append(f"{seconds}s")
    
    return " ".join(parts)

def chunk_message(content, chunk_size=2000):
    """
    Split a message into chunks to avoid Discord's message length limit.
    
    Args:
        content (str): Message content
        chunk_size (int): Maximum chunk size
        
    Returns:
        list: List of message chunks
    """
    return [content[i:i + chunk_size] for i in range(0, len(content), chunk_size)]