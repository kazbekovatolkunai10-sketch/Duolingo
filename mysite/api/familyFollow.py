from fastapi import APIRouter, Depends, HTTPException
from mysite.database.models import FamilyFollow
from mysite.database.schema import FamilyFollowOutSchema, FamilyFollowInputSchema
from mysite.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List

family_follow_router = APIRouter(prefix='/family_follow', tags=['Family Follow'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@family_follow_router.post('/', response_model=FamilyFollowOutSchema)
async def create_family_follow(family_follow: FamilyFollowInputSchema, db: Session = Depends(get_db)):
    family_follow_db = FamilyFollow(**family_follow.dict())
    db.add(family_follow_db)
    db.commit()
    db.refresh(family_follow_db)
    return family_follow_db


@family_follow_router.get('/', response_model=List[FamilyFollowOutSchema])
async def list_famil_follow(db: Session = Depends(get_db)):
    return db.query(FamilyFollow).all()


@family_follow_router.get('/{family_follow_id}/', response_model=FamilyFollowOutSchema)
async def detail_family_follow(family_follow_id: int, db: Session = Depends(get_db)):
    family_follow_db = db.query(FamilyFollow).filter(FamilyFollow.id == family_follow_id).first()
    if not family_follow_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)

    return family_follow_db


@family_follow_router.put('/{family_follow_id}/', response_model=dict)
async def update_family_follow(family_follow_id: int, family_follow: FamilyFollowInputSchema,
                             db: Session = Depends(get_db)):
    family_follow_db = db.query(FamilyFollow).filter(FamilyFollow.id == family_follow_id).first()
    if not family_follow_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)

    for family_follow_key, family_follow_value in family_follow.dict().items():
        setattr(family_follow_db, family_follow_key, family_follow_value)

    db.commit()
    db.refresh(family_follow_db)
    return {'message': 'Успешно изменено'}


@family_follow_router.delete('/{family_follow_id}/', response_model=dict)
async def detail_family_follow(family_follow_id: int, db: Session = Depends(get_db)):
    family_follow_db = db.query(FamilyFollow).filter(FamilyFollow.id == family_follow_id).first()
    if not family_follow_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)

    db.delete(family_follow_db)
    db.commit()
    return {'message': 'Успешно удалено'}
