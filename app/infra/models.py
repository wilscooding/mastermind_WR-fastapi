from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Boolean
from sqlalchemy.types import JSON
from sqlalchemy.orm import relationship
from app.infra.database import Base
from datetime import datetime

"""SQLAlchemy ORM models for User, Game, and LeaderboardEntry."""


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    secret = Column(JSON, nullable=False)
    attempts_used = Column(Integer, default=0)
    history = Column(JSON, default=lambda: [])
    won = Column(Boolean, default=False)
    lost = Column(Boolean, default=False)
    mode = Column(String, default='fallback')

    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    user = relationship("User", back_populates="games")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    leaderboard_entries = relationship("LeaderboardEntry", back_populates="user")
    games = relationship("Game", back_populates="user")

class LeaderboardEntry(Base):
    __tablename__ = "leaderboard"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    score = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="leaderboard_entries")

