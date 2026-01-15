from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from Duolingo.mysite.database.models import LessonLevel, UserProfile
from Duolingo.mysite.database.schema import LessonLevelOutSchema
from Duolingo.mysite.database.db import SessionLocal
from Duolingo.mysite.api.deps import get_current_user

lesson_level_router = APIRouter(prefix='/lesson_levels', tags=['Lesson Levels'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@lesson_level_router.get('/', response_model=List[LessonLevelOutSchema])
async def list_lesson_level(user: UserProfile = Depends(get_current_user),
                         db: Session = Depends(get_db)):
    return db.query(LessonLevel).filter(LessonLevel.user_id == user.id).all()


@lesson_level_router.get('/{lesson_id}/', response_model=LessonLevelOutSchema)
async def detail_lesson_level(lesson_id: int, user: UserProfile = Depends(get_current_user),
                              db: Session = Depends(get_db)):
    lesson_level = db.query(LessonLevel).filter(
        LessonLevel.user_id == user.id,
        LessonLevel.lesson_id == lesson_id
    ).first()

    if not lesson_level:
        raise HTTPException(status_code=400, detail='Уровень по этому уроку не найден')

    return lesson_level

