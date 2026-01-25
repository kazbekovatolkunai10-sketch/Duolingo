from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from mysite.config import (
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_DAYS,
)
from mysite.database.db import SessionLocal
from mysite.database.models import UserProfile, RefreshToken
from mysite.database.schema import (
    UserCreateSchema,
    UserLoginSchema,
    UserProfileOutSchema,   # сделай Out без password
    TokenPairOut,           # access_token/refresh_token/token_type
)


auth_router = APIRouter(prefix="/auth", tags=["Auth"])
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


# =========================
# DB
# =========================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================
# JWT utils
# =========================
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: dict) -> str:
    return create_access_token(
        data=data,
        expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
    )


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)


# =========================
# Schemas for auth actions
# =========================
from pydantic import BaseModel

class LogoutIn(BaseModel):
    refresh_token: str

class RefreshIn(BaseModel):
    refresh_token: str


# =========================
# ROUTES
# =========================
@auth_router.post("/register", response_model=UserProfileOutSchema, status_code=201)
def register(user: UserCreateSchema, db: Session = Depends(get_db)):
    exists_email = db.query(UserProfile).filter(UserProfile.email == user.email).first()
    if exists_email:
        raise HTTPException(status_code=400, detail="Email already exists")

    exists_username = db.query(UserProfile).filter(UserProfile.username == user.username).first()
    if exists_username:
        raise HTTPException(status_code=400, detail="Username already exists")

    new_user = UserProfile(
        email=user.email,
        username=user.username,
        password=get_password_hash(user.password),
        is_active=True,  # если не нужна активация по коду
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@auth_router.post("/login", response_model=TokenPairOut)
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
        "token_type": "bearer",
    }


@auth_router.post("/refresh", response_model=TokenPairOut)
def refresh_tokens(payload: RefreshIn, db: Session = Depends(get_db)):
    # 1) проверяем что refresh существует в БД
    token_row = db.query(RefreshToken).filter(RefreshToken.token == payload.refresh_token).first()
    if not token_row:
        raise HTTPException(status_code=401, detail="Refresh token is invalid or revoked")

    # 2) проверяем JWT валидность/exp
    decoded = decode_token(payload.refresh_token)
    user_id = decoded.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    # 3) выдаём новую пару токенов
    new_access = create_access_token({"sub": str(user_id)})
    new_refresh = create_refresh_token({"sub": str(user_id)})

    # 4) ротируем refresh (старый удаляем, новый сохраняем)
    db.delete(token_row)
    db.add(RefreshToken(token=new_refresh, user_id=int(user_id)))
    db.commit()

    return {
        "access_token": new_access,
        "refresh_token": new_refresh,
        "token_type": "bearer",
    }


@auth_router.post("/logout")
def logout(payload: LogoutIn, db: Session = Depends(get_db)):
    token_row = db.query(RefreshToken).filter(RefreshToken.token == payload.refresh_token).first()
    if not token_row:
        raise HTTPException(status_code=404, detail="Token not found")

    db.delete(token_row)
    db.commit()
    return {"message": "logged out"}
