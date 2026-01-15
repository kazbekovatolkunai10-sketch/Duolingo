from fastapi import  APIRouter, Depends, HTTPException
from Duolingo.mysite.database.models import UserProfile, RefreshToken
from Duolingo.mysite.database.schema import UserProfileInputSchema, UserProfileOutSchema, UserProfileLoginSchema
from Duolingo.mysite.database.db import SessionLocal
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from Duolingo.mysite.config import (SECRET_KEY, ALGORITHM,
                                    ACCESS_TOKEN_LIFETIME,
                                    REFRESH_TOKEN_LIFETIME)
from datetime import timedelta, datetime
from jose import jwt
from typing import Optional


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_schema = OAuth2PasswordBearer(tokenUrl='/auth/login')


auth_router = APIRouter(prefix='/auth', tags=['Auth'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(ACCESS_TOKEN_LIFETIME)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict):
    return create_access_token(data, expires_delta=timedelta(days=REFRESH_TOKEN_LIFETIME))


@auth_router.post('/register/', response_model=dict)
async def register(user: UserProfileInputSchema, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.username == user.username).first()
    email_db = db.query(UserProfile).filter(UserProfile.email == user.email).first()
    if user_db:
        raise HTTPException(detail='Мындай username бар экен', status_code=400)
    elif email_db:
        raise HTTPException(detail='Мындай email бар экен', status_code=400)

    hash_password = get_password_hash(user.password)
    user_data = UserProfile(
        avatar = user.avatar,
        first_name = user.first_name,
        last_name = user.last_name,
        username = user.username,
        email = user.email,
        password = hash_password,
        phone_number = user.phone_number,
        is_active = user.is_active
    )
    db.add(user_data)
    db.commit()
    db.refresh(user_data)
    return {'message': 'Вы успешно зарегистрированы'}


@auth_router.post('/login/', response_model=dict)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.username == form_data.username).first()
    if not user_db or not verify_password(form_data.password, user_db.password):
        raise HTTPException(detail='Сиз жазган маалымат туура эмес', status_code=401)

    access_token = create_access_token({'sub': user_db.username})
    refresh_token = create_refresh_token({'sub': user_db.username})

    token_db = RefreshToken(user_id=user_db.id, token=refresh_token)
    db.add(token_db)
    db.commit()

    return {'access_token': access_token, 'refresh_token': refresh_token, 'token_type': 'Bearer'}


@auth_router.post('/logout/', response_model=dict)
async def logout(refresh_token: str, db: Session = Depends(get_db)):
    stored_token = db.query(RefreshToken).filter(RefreshToken.token == refresh_token).first()

    if not stored_token:
        raise HTTPException(detail='Маалымат туура эмес', status_code=401)

    db.delete(stored_token)
    db.commit()
    return {'message': 'Вы вышли'}


@auth_router.post('/refresh_token/', response_model=dict)
async def logout(refresh_token: str, db: Session = Depends(get_db)):
    stored_token = db.query(RefreshToken).filter(RefreshToken.token == refresh_token).first()

    if not stored_token:
        raise HTTPException(detail='Маалымат туура эмес', status_code=401)

    access_token = create_access_token({'sub': stored_token.id})

    return {'access_token': access_token, 'token_type': 'Bearer'}
