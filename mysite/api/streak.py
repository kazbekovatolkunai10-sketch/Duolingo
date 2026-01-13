from fastapi import APIRouter, Depends, HTTPException
from Duolingo.mysite.database.models import Streak
from Duolingo.mysite.database.schema import StreakOutSchema, StreakInputSchema
from Duolingo.mysite.database.db import SessionLocal
from typing import List
from sqlalchemy.orm import Session

streak_router = APIRouter(prefix='/streak', tags=['Streak'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@streak_router.post('/', response_model=StreakOutSchema)
async def create_streak(streak: StreakInputSchema, db: Session = Depends(get_db)):
    streak_db = Streak(**streak.dict())
    db.add(streak_db)
    db.commit()
    db.refresh(sjbgmjk
    return user_progress_dbazzzz


@user_progress_router.get('/', response_model=List[UserProgressOutSchema])
async def list_user_progress(db: Session = Depends(get_db)):
    return db.query(UserProgres).all()


@user_progress_router.get('/{user_progress_id}/', response_model=UserProgressOutSchema)
async def detail_user_progress(user_progress_id: int, db: Session = Depends(get_db)):
    user_progress_db = db.query(UserProgres).filter(UserProgres.id == user_progress_id).first()
    if not user_progress_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)

    return user_progress_db


@user_progress_router.put('/{user_progress_id}/', response_model=dict)
async def update_user_progress(user_progress_id: int, achievement: UserProgressInputSchema,
                             db: Session = Depends(get_db)):
    user_progress_db = db.query(UserProgres).filter(UserProgres.id == user_progress_id).first()
    if not user_progress_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)

    for achievement_key, achievement_value in achievement.dict().items():
        setattr(user_progress_db, achievement_key, achievement_value)

    db.commit()
    db.refresh(user_progress_db)
    return {'message': 'Успешно изменено'}


@user_progress_router.delete('/{achievement_id}/', response_model=dict)
async def delete_achievement(achievement_id: int, db: Session = Depends(get_db)):
    user_progress_db = db.query(UserProgres).filter(UserProgres.id == achievement_id).first()
    if not user_progress_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)

    db.delete(user_progress_db)
    db.commit()
    return {'message': 'Успешно удалено'}
