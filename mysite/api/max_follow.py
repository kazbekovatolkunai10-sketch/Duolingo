from fastapi import APIRouter, Depends, HTTPException
from Duolingo.mysite.database.models import MaxFollow
from Duolingo.mysite.database.schema import MaxFollowOutSchema, MaxFollowInputSchema
from Duolingo.mysite.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List

max_follow_router = APIRouter(prefix='/max_follow', tags=['Max Follow'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@max_follow_router.post('/', response_model=MaxFollowOutSchema)
async def create_max_follow(max_follow: MaxFollowInputSchema, db: Session = Depends(get_db)):
    MaxFollow.db = MaxFollow(**MaxFollow.dict())
    db.add(MaxFollow.db)
    db.commit()
    db.refresh(MaxFollow.db)
    return MaxFollow.db

@max_follow_router.get('/', response_model=List[MaxFollowOutSchema])
async def list_max_follow(db: Session = Depends(get_db)):
    return db.query(MaxFollow).all()


@max_follow_router.get('/{max_follow_id}/', response_model=MaxFollowOutSchema)
async def detail_max_follow(max_follow_id: int, db: Session = Depends(get_db)):
    max_follow_db = db.query(MaxFollow).filter(MaxFollow.id == max_follow_id).first()
    if not max_follow_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)

    return max_follow_db


@max_follow_router.put('/{max_follow_id}/', response_model=dict)
async def detail_max_follow(max_follow_id: int, max_follow: MaxFollowInputSchema, db: Session = Depends(get_db)):
    max_follow_db = db.query(MaxFollow).filter(MaxFollow.id == max_follow_id).first()
    if not max_follow_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)

    for max_follow_key, max_follow_value in max_follow.dict().items():
        setattr(max_follow_db, max_follow_key, max_follow_value)

    db.commit()
    db.refresh(max_follow_db)
    return {'message': 'Успешно изменено'}


@max_follow_router.delete('/{max_follow_id}/', response_model=dict)
async def detail_max_follow(max_follow_id: int, db: Session = Depends(get_db)):
    max_follow_db = db.query(MaxFollow).filter(MaxFollow.id == max_follow_id).first()
    if not max_follow_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)

    db.delete(max_follow_db)
    db.commit()
    return {'message': 'Успешно удалено'}