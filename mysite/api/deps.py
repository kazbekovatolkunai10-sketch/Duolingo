from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from Duolingo.mysite.api.auth import oauth2_schema
from Duolingo.mysite.database.db import SessionLocal
from Duolingo.mysite.database.models import UserProfile
from Duolingo.mysite.config import SECRET_KEY, ALGORITHM

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    token: str = Depends(oauth2_schema),
    db: Session = Depends(get_db)
) -> UserProfile:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str | None = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = (
        db.query(UserProfile)
        .filter(UserProfile.username == username).first()
    )

    if user is None:
        raise credentials_exception

    return user
