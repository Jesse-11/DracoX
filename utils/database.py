"""
Database utilities for the Discord bot.
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from contextlib import asynccontextmanager

import config

# Base class for SQLAlchemy models
Base = declarative_base()

# Create async engine
engine = create_async_engine(config.DATABASE_URL, echo=False)

# Session factory
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

@asynccontextmanager
async def get_db_session():
    """
    Provide a transactional scope around a series of operations.
    
    Yields:
        AsyncSession: Database session
    """
    session = async_session()
    try:
        yield session
    finally:
        await session.close()

async def init_db():
    """
    Initialize the database, creating tables if they don't exist.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)