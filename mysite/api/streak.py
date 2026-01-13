from fastapi import APIRouter, Depends, HTTPException
from Duolingo.mysite.database.models import Streak
from Duolingo.mysite.database.schema import StreakInputSchema, StreakOutSchema
from Duolingo.mysite.database.db import SessionLocal
from typing import List
from sqlalchemy.orm import Session

Streak_router = APIRouter(prefix='/Streak', tags=['Streak'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@Streak_router.post('/', response_model=StreakOutSchema)
async def create_familyFollow(familyFollow: StreakInputSchema, db: Session = Depends(get_db)):
    Streak.db = Streak(**Streak.dict())
    db.add(Streak.db)
    db.commit()
    db.refresh(Streak.db)
    return Streak.db

@Streak_router.get('/', response_model=List[StreakOutSchema])
async def list_Streak(db: Session = Depends(get_db)):
    return db.query(Streak).all()


@Streak_router.get('/{Streak_id}/', response_model=StreakOutSchema)
async def detail_Streak(Streak_id: int, db: Session = Depends(get_db)):
    Streak_db = db.query(Streak).filter(Streak.id == Streak_id).first()
    if not Streak_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)

    return Streak_db

@Streak_router.put('/{Streak_id}/', response_model=dict)
async def update_Streak(Streak_id: int, Streak: StreakInputSchema,
                             db: Session = Depends(get_db)):
    Streak_db = db.query(Streak).filter(Streak.id == Streak_id).first()
    if not Streak_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)

    for Streak_key, Streak_value in Streak.dict().items():
        setattr(Streak_db, Streak_key, Streak_value)

    db.commit()
    db.refresh(Streak_db)
    return {'message': 'Успешно изменено'}





@Streak_router.delete('/{Streak_id}/', response_model=dict)
async def delete_Streak(Streak_id: int, db: Session = Depends(get_db)):
    Streak_db = db.query(Streak).filter(Streak.id == Streak_id).first()
    if not Streak_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)

    db.delete(Streak_db)
    db.commit()
    return {'message': 'Успешно удалено'}
