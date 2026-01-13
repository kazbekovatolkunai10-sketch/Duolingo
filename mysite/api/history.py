from fastapi import APIRouter, Depends, HTTPException
from Duolingo.mysite.database.models import XPHistory
from Duolingo.mysite.database.schema import XPHistoryOutSchema, XPHistoryInputSchema
from Duolingo.mysite.database.db import SessionLocal
from typing import List
from sqlalchemy.orm import Session

history_router = APIRouter(prefix='/history', tags=['History'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@history_router.post('/', response_model=XPHistoryOutSchema)
async def create_history(history: XPHistoryInputSchema, db: Session = Depends(get_db)):
    history_db = XPHistory(**history.dict())
    db.add(history_db)
    db.commit()
    db.refresh(history_db)
    return history_db


@history_router.get('/', response_model=List[XPHistoryOutSchema])
async def list_history(db: Session = Depends(get_db)):
    return db.query(XPHistory).all()


@history_router.get('/{history_id}/', response_model=XPHistoryOutSchema)
async def detail_history(history_id: int, db: Session = Depends(get_db)):
    history_db = db.query(XPHistory).filter(XPHistory.id == history_id).first()
    if not history_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)

    return history_db


@history_router.put('/{history_id}/', response_model=dict)
async def update_history(history_id: int, achievement: XPHistoryInputSchema,
                             db: Session = Depends(get_db)):
    history_db = db.query(XPHistory).filter(XPHistory.id == history_id).first()
    if not history_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)

    for achievement_key, achievement_value in achievement.dict().items():
        setattr(history_db, achievement_key, achievement_value)

    db.commit()
    db.refresh(history_db)
    return {'message': 'Успешно изменено'}


@history_router.delete('/{history_id}/', response_model=dict)
async def delete_achievement(history_id: int, db: Session = Depends(get_db)):
    history_db = db.query(XPHistory).filter(XPHistory.id == history_id).first()
    if not history_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)

    db.delete(history_db)
    db.commit()
    return {'message': 'Успешно удалено'}
