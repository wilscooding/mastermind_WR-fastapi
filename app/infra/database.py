from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base, Session

DATABASE_URL = 'sqlite:///./mastermind.db'

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()

def get_database() -> Session:
    database = sessionLocal()
    try:
        yield database
    finally:
        database.close()

def test_db_connection():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception as e:
        print("DB connection failed:", e)
        return False