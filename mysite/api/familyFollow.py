from fastapi import APIRouter, Depends, HTTPException
from Duolingo.mysite.database.models import FamilyFollow
from Duolingo.mysite.database.schema import FamilyFollowOutSchema, FamilyFollowInputSchema
from Duolingo.mysite.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List

familyFollow_router = APIRouter(prefix='/familyFollow', tags=['FamilyFollow'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@familyFollow_router.post('/', response_model=FamilyFollowOutSchema)
async def create_familyFollow(familyFollow: FamilyFollowInputSchema, db: Session = Depends(get_db)):
    FamilyFollow.db = FamilyFollow(**FamilyFollow.dict())
    db.add(familyFollow.db)
    db.commit()
    db.refresh(familyFollow.db)
    return familyFollow.db


@familyFollow_router.get('/', response_model=List[FamilyFollowOutSchema])
async def list_familyFollow(db: Session = Depends(get_db)):
    return db.query(FamilyFollow).all()


@familyFollow_router.get('/{familyFollow_id}/', response_model=FamilyFollowOutSchema)
async def detail_familyFollow(familyFollow_id: int, db: Session = Depends(get_db)):
    FamilyFollow_db = db.query(FamilyFollow).filter(FamilyFollow.id == familyFollow_id).first()
    if not FamilyFollow_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)

    return FamilyFollow_db


@familyFollow_router.put('/{familyFollow_id}/', response_model=dict)
async def update_familyFollow(familyFollow_id: int, familyFollow: FamilyFollowInputSchema,
                             db: Session = Depends(get_db)):
    familyFollow_db = db.query(FamilyFollow).filter(FamilyFollow.id == familyFollow_id).first()
    if not familyFollow_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)

    for familyFollow_key, familyFollow_value in familyFollow.dict().items():
        setattr(familyFollow_db, familyFollow_key, familyFollow_value)

    db.commit()
    db.refresh(familyFollow_db)
    return {'message': 'Успешно изменено'}





@familyFollow_router.delete('/{familyFollow_id}/', response_model=dict)
async def delete_familyFollow(familyFollow_id: int, db: Session = Depends(get_db)):
    familyFollow_db = db.query(FamilyFollow).filter(FamilyFollow.id == familyFollow_id).first()
    if not familyFollow_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)

    db.delete(familyFollow_db)
    db.commit()
    return {'message': 'Успешно удалено'}