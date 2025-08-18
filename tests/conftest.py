import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.infra.database import Base
from fastapi.testclient import TestClient
from app.main import app
from app.api.deps import get_database
from app.infra.models import User
from app.infra.sqlalchemy_game_repo import SQLAlchemyGameRepository
from app.infra.local_random import LocalRandomSecretProvider
from app.services.game_service import GameService

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_database] = override_get_db

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture()
def client():
    return TestClient(app)

@pytest.fixture()
def database_session():
    database = TestingSessionLocal()
    try:
        yield database
    finally:
        database.close()



@pytest.fixture()
def test_user_factory(database_session: Session):
    """
    Factory for creating test users in the DB.
    Usage: user = test_user_factory(username="bob", email="bob@example.com")
    """
    def create_user(username="user", email="user@example.com", password="password123"):
        user = User(
            username=username,
            email=email,
            hashed_password=password  
        )
        database_session.add(user)
        database_session.commit()
        database_session.refresh(user)
        return user

    return create_user

@pytest.fixture()
def game_service(database_session):
    repo = SQLAlchemyGameRepository(database_session)
    secret_provider = LocalRandomSecretProvider()
    return GameService(repo, secret_provider)

