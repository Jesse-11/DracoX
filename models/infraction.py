"""
Infraction model for the Discord bot.
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func

from utils.database import Base

class Infraction(Base):
    """
    Represents a moderation action taken against a user.
    """
    __tablename__ = 'infractions'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(String, nullable=False)
    guild_id = Column(String, nullable=False)
    moderator_id = Column(String, nullable=False)
    
    # Infraction details
    type = Column(String, nullable=False)  # 'warn', 'mute', 'kick', 'ban'
    reason = Column(String, nullable=True)
    
    # Timestamps
    timestamp = Column(DateTime, server_default=func.now())
    expires_at = Column(DateTime, nullable=True)  # For temporary actions
    
    def __repr__(self):
        return f"<Infraction(user_id={self.user_id}, type={self.type})>"