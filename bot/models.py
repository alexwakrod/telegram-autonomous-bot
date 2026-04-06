from sqlalchemy import Column, Integer, BigInteger, String, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")  # postgresql+asyncpg://...

Base = declarative_base()

class CommandLog(Base):
    __tablename__ = 'command_logs'
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, nullable=False)   # BIGINT
    command = Column(String(50), nullable=False)
    timestamp = Column(DateTime, nullable=False)

class Reminder(Base):
    __tablename__ = 'reminders'
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, nullable=False)
    chat_id = Column(BigInteger, nullable=False)
    remind_at = Column(DateTime, nullable=False)
    message = Column(Text, nullable=False)
    done = Column(Boolean, default=False)

class ModerationRule(Base):
    __tablename__ = 'moderation_rules'
    id = Column(Integer, primary_key=True)
    rule_type = Column(String(10), nullable=False)
    threshold = Column(Integer, nullable=False)
    duration_minutes = Column(Integer, nullable=True)
    enabled = Column(Boolean, default=True)

# Async engine
engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)