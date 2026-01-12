from fastapi import APIRouter, Depends, HTTPException
from Duolingo.mysite.database.models import Achievement
from Duolingo.mysite.database.schema import AchievementInputSchema, AchievementOutSchema
from Duolingo.mysite.database.db import SessionLocal
from typing import List
from sqlalchemy.orm import Session

achievement_router = APIRouter(prefix='/achievements', tags=['Achievements'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@achievement_router.post('/', response_model=AchievementOutSchema)
async def create_achievement(achievement: AchievementInputSchema, db: Session = Depends(get_db)):
    achievement_db = Achievement(**achievement.dict())
    db.add(achievement_db)
    db.commit()
    db.refresh(achievement_db)
    return achievement_db


@achievement_router.get('/', response_model=AchievementOutSchema)
async def list_achievement(db: Session = Depends(get_db)):
    return db.query(Achievement).all()


@achievement_router.get('/{achievement_id}/', response_model=AchievementOutSchema)
async def detail_achievement(achievement_id: int, db: Session = Depends(get_db)):
    achievement_db = db.query(Achievement).filter(Achievement.id == achievement_id).first()
    if not achievement_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)

    return achievement_db


@achievement_router.put('/{achievement_id}/', response_model=dict)
async def update_achievement(achievement_id: int, achievement: AchievementInputSchema,
                             db: Session = Depends(get_db)):
    achievement_db = db.query(Achievement).filter(Achievement.id == achievement_id).first()
    if not achievement_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)

    for achievement_key, achievement_value in achievement.dict().items():
        setattr(achievement_db, achievement_key, achievement_value)

    db.commit()
    db.refresh(achievement_db)
    return {'message': 'Успешно изменено'}


@achievement_router.delete('/{achievement_id}/', response_model=dict)
async def delete_achievement(achievement_id: int, db: Session = Depends(get_db)):
    achievement_db = db.query(Achievement).filter(Achievement.id == achievement_id).first()
    if not achievement_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)

    db.delete(achievement_db)
    db.commit()
    return {'message': 'Успешно удалено'}
