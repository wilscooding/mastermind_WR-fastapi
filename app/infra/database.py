from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base, Session

"""SQLAlchemy database configuration and session management."""


DATABASE_URL = 'sqlite:///./mastermind.db'

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()

