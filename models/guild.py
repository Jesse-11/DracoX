"""
Guild model for the Discord bot.
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func

from utils.database import Base

class Guild(Base):
    """
    Represents a Discord guild (server) configuration.
    """
    __tablename__ = 'guilds'
    
    id = Column(Integer, primary_key=True)
    guild_id = Column(String, unique=True, nullable=False)
    prefix = Column(String, default='!')
    
    # Moderation settings
    mod_role_id = Column(String, nullable=True)
    mute_role_id = Column(String, nullable=True)
    log_channel_id = Column(String, nullable=True)
    
    # Welcome settings
    welcome_enabled = Column(Boolean, default=False)
    welcome_channel_id = Column(String, nullable=True)
    welcome_message = Column(String, nullable=True)
    
    # Auto-moderation settings
    automod_enabled = Column(Boolean, default=False)
    filter_invites = Column(Boolean, default=False)
    filter_links = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    def __repr__(self):
        return f"<Guild(guild_id={self.guild_id}, prefix={self.prefix})>"