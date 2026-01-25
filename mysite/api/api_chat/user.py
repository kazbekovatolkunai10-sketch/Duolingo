from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from typing import List

from mysite.database.db import SessionLocal
from mysite.database.models import UserProfile
from mysite.database.schema import UserResponseSchema, UserProfileOutSchema, UserProfileInputSchema

user_router = APIRouter(prefix="/user", tags=["User"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@user_router.get("/", response_model=List[UserResponseSchema])
def users(db: Session = Depends(get_db)):
    return db.query(UserProfile).all()


@user_router.get("/{user_id}", response_model=UserResponseSchema)
def user_detail(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Not found")
    return user


@user_router.put("/{user_id}/", response_model=dict)
def update_user(user_id: int, user: UserProfileInputSchema, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if not user_db:
        raise HTTPException(status_code=404, detail="Not found")

    for key, value in user.model_dump(exclude_unset=True).items():
        setattr(user_db, key, value)

    db.commit()
    db.refresh(user_db)
    return {"message": "Updated"}


@user_router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(user)
    db.commit()
    return {"message": "deleted"}