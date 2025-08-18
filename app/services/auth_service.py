from datetime import datetime, timedelta
import os
from jose import JWTError, jwt
from passlib.context import CryptContext
from dotenv import load_dotenv

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.infra.database import get_database
from app.infra import models

load_dotenv()

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.getenv("SECRET_KEY", "devsecret")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

def hash_password(password: str) -> str:
    return password_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool: 
    return password_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_in: timedelta = None):
    to_encode = data.copy()
    expires_delta = datetime.utcnow() + (expires_in or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expires_delta})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str):
    try: 
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError as e:
        print(f"Token decode error: {e}")
        return None
    

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_database)) -> models.User:
    user_id = decode_access_token(token)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    user = db.query(models.User).filter(models.User.email == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return user
