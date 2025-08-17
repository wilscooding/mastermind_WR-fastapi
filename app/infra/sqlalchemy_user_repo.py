from sqlalchemy.orm import Session
from app.infra.models import User
from app.services.auth_service import hash_password

class SQLAlchemyUserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_username(self, username: str):
        return self.db.query(User).filter(User.username == username).first()

    def get_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()

    def create_user(self, username: str, email: str, password: str):
        new_user = User(
            username=username,
            email=email,
            hashed_password=hash_password(password),
        )
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user
