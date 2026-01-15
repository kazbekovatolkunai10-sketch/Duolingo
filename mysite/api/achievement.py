from fastapi import APIRouter, Depends, HTTPException
from Duolingo.mysite.database.models import Achievement, UserAchievement
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


def give_achievement_if_not_exists(db: Session, user_id: int, code: str) -> bool:
    achievement = db.query(Achievement).filter(Achievement.code == code).first()
    if not achievement:
        return False

    exists = db.query(UserAchievement).filter(
        UserAchievement.user_id == user_id,
        UserAchievement.achievement_id == achievement.id
    ).first()

    if exists:
        return False

    # Выдаём
    db.add(UserAchievement(user_id=user_id, achievement_id=achievement.id))
    return True


@achievement_router.get('/', response_model=List[AchievementOutSchema])
async def list_achievement(db: Session = Depends(get_db)):
    return db.query(Achievement).all()


@achievement_router.get('/{achievement_id}/', response_model=AchievementOutSchema)
async def detail_achievement(achievement_id: int, db: Session = Depends(get_db)):
    achievement_db = db.query(Achievement).filter(Achievement.id == achievement_id).first()
    if not achievement_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)

    return achievement_db

