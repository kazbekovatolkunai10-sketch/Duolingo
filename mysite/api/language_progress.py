from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from Duolingo.mysite.database.models import LanguageProgress, UserProfile
from Duolingo.mysite.database.schema import LanguageProgressOutSchema
from Duolingo.mysite.database.db import SessionLocal
from Duolingo.mysite.api.deps import get_current_user

language_progress_router = APIRouter(prefix='/language_progress', tags=['Language Progress'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@language_progress_router.get('/', response_model=List[LanguageProgressOutSchema])
async def list_language_level(user: UserProfile = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(LanguageProgress).filter(LanguageProgress.user_id == user.id).all()


@language_progress_router.get('/{lesson_id}/', response_model=LanguageProgressOutSchema)
async def detail_lesson_level(language_id: int, user: UserProfile = Depends(get_current_user),
                              db: Session = Depends(get_db)):
    language_progress = db.query(LanguageProgress).filter(LanguageProgress.user_id == user.id, LanguageProgress.language_id == language_id).first()

    if not language_progress:
        raise HTTPException(status_code=400, detail='Уровень по этому уроку не найден')

    return language_progress
