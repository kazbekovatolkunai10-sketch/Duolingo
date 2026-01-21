from jose import jwt
from passlib.context import CryptContext
from datetime import timedelta, datetime
from typing import Optional
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from mysite.database.db import SessionLocal
from mysite.database.models_chat import UserProfile, RefreshToken
from mysite.database.schema_chat import UserCreateSchema, UserLoginSchema
from mysite.config import (
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_DAYS
)

auth_router = APIRouter(prefix="/auth", tags=["Auth"])

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: dict):
    return create_access_token(
        data,
        expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)


@auth_router.post("/register")
def register(user: UserCreateSchema, db: Session = Depends(get_db)):
    if db.query(UserProfile).filter(UserProfile.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")

    new_user = UserProfile(
        email=user.email,
        username=user.username,
        password=get_password_hash(user.password)
    )
    db.add(new_user)
    db.commit()
    return {"message": "created"}


@auth_router.post("/login")
def login(data: UserLoginSchema, db: Session = Depends(get_db)):
    user = db.query(UserProfile).filter(UserProfile.email == data.email).first()
    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})

    db.add(RefreshToken(token=refresh_token, user_id=user.id))
    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@auth_router.post("/logout")
def logout(refresh_token: str, db: Session = Depends(get_db)):
    token = db.query(RefreshToken).filter(RefreshToken.token == refresh_token).first()
    if not token:
        raise HTTPException(status_code=404, detail="Token not found")
    db.delete(token)
    db.commit()
    return {"message": "logged out"}