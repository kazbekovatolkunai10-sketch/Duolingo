from fastapi import APIRouter, Depends, HTTPException
from mysite.database.models import UserProfile
from mysite.database.schema import UserProfileInputSchema, UserProfileOutSchema
from mysite.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List


user_router = APIRouter(prefix="/users", tags=["User CRUD"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@user_router.get("/", response_model=List[UserProfileOutSchema])
def list_user(db: Session = Depends(get_db)):
    users = db.query(UserProfile).order_by(UserProfile.id.desc()).all()
    return users


@user_router.get("/{user_id}/", response_model=UserProfileOutSchema)
def detail_user(user_id: int, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if not user_db:
        raise HTTPException(detail="маалымат жок", status_code=404)
    return user_db


@user_router.put("/{user_id}/", response_model=dict)
def update_user(user_id: int, user: UserProfileInputSchema, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if not user_db:
        raise HTTPException(status_code=404, detail="Мындай колдонуучу жок")

    for key, value in user.model_dump(exclude_unset=True).items():  # ✅ pydantic v2 safe
        setattr(user_db, key, value)

    db.commit()
    db.refresh(user_db)
    return {"message": "Колдонуучу өзгөртүлдү"}


@user_router.delete("/{user_id}/", response_model=dict)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if not user_db:
        raise HTTPException(detail="Мындай колдонуучу жок", status_code=404)

    db.delete(user_db)
    db.commit()
    return {"message": "Колдонуучу өчүрүлдү"}
