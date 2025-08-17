from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.types import JSON
from app.infra.database import Base

class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    secret = Column(JSON, nullable=False)
    attempts_used = Column(Integer, default=0)
    history = Column(JSON, default=lambda: [])
    won = Column(Boolean, default=False)
    lost = Column(Boolean, default=False)
    mode = Column(String, default='fallback')
    

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)