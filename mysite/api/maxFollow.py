from fastapi import APIRouter, Depends, HTTPException
from Duolingo.mysite.database.models import MaxFollow
from Duolingo.mysite.database.schema import MaxFollowOutSchema, MaxFollowInputSchema
from Duolingo.mysite.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List

MaxFollow_router = APIRouter(prefix='/MaxFollow', tags=['MaxFollow'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@MaxFollow_router.post('/', response_model=MaxFollowOutSchema
)
async def create_familyFollow(familyFollow: MaxFollowInputSchema, db: Session = Depends(get_db)):
    MaxFollow.db = MaxFollow(**MaxFollow.dict())
    db.add(MaxFollow.db)
    db.commit()
    db.refresh(MaxFollow.db)
    return MaxFollow.db

@MaxFollow_router.get('/', response_model=List[MaxFollowOutSchema])
async def list_MaxFollow(db: Session = Depends(get_db)):
    return db.query(MaxFollow).all()


@MaxFollow_router.get('/{MaxFollow_id}/', response_model=MaxFollowOutSchema)
async def detail_MaxFollow(MaxFollow_id: int, db: Session = Depends(get_db)):
    MaxFollow_db = db.query(MaxFollow).filter(MaxFollow.id == MaxFollow_id).first()
    if not MaxFollow_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)

    return MaxFollow_db


@MaxFollow_router.put('/{MaxFollow_id}/', response_model=dict)
async def update_MaxFollow(MaxFollow_id: int, MaxFollow: MaxFollowInputSchema,
                             db: Session = Depends(get_db)):
    MaxFollow_db = db.query(MaxFollow).filter(MaxFollow.id == MaxFollow_id).first()
    if not MaxFollow.db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)

    for MaxFollow_key, MaxFollow_value in MaxFollow.dict().items():
        setattr(MaxFollow_db, MaxFollow_key, MaxFollow_value)

    db.commit()
    db.refresh(MaxFollow_db)
    return {'message': 'Успешно изменено'}





@MaxFollow_router.delete('/{MaxFollow_id}/', response_model=dict)
async def delete_MaxFollow(MaxFollow_id: int, db: Session = Depends(get_db)):
    MaxFollow_db = db.query(MaxFollow).filter(MaxFollow.id == MaxFollow_id).first()
    if not MaxFollow_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)

    db.delete(MaxFollow)
    db.commit()
    return {'message': 'Успешно удалено'}