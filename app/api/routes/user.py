import email
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.infra.database import sessionLocal
from app.infra.models import User
from app.services.auth_service import hash_password, verify_password, create_access_token
from app.api.schemas import UserSignup, UserLogin
from app.api.deps import get_database

router = APIRouter(prefix="/users", tags=["users"])



@router.post("/signup") 
def register_user(body: UserSignup, database: Session = Depends(get_database)):
    user = database.query(User).filter(User.email == body.email).first()
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = User(username=body.username, email=body.email, hashed_password=hash_password(body.password))
    database.add(new_user)
    database.commit()
    database.refresh(new_user)
    return {"id": new_user.id, "username": new_user.username, "email": new_user.email}

@router.post("/login")
def login_user(body: UserLogin, database: Session = Depends(get_database)):
    user = database.query(User).filter(User.email == body.email).first()
    if not user or not verify_password(body.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = create_access_token(data={"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}