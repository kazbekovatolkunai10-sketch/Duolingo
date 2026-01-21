from fastapi import APIRouter, Depends, HTTPException
from mysite.database.models import SuperFollow
from mysite.database.schema import SuperFollowOutSchema, SuperFollowInputSchema
from mysite.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List

super_follow_router = APIRouter(prefix='/super_follow', tags=['Super Follow'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@super_follow_router.post('/', response_model=SuperFollowOutSchema)
def create_follow(
    follow: SuperFollowInputSchema, db: Session = Depends(get_db)):

    follow = SuperFollow(**follow.dict())
    db.add(follow)
    db.commit()
    db.refresh(follow)
    return follow


@super_follow_router.get('/', response_model=List[SuperFollowOutSchema])
async def list_super_follow(db: Session = Depends(get_db)):
    return db.query(SuperFollow).all()


@super_follow_router.get('/{super_follow_id}/', response_model=SuperFollowOutSchema)
async def detail_user(super_follow_id: int, db: Session = Depends(get_db)):
    super_follow_db = db.query(SuperFollow).filter(SuperFollow.id == super_follow_id).first()

    if not super_follow_db:
        raise HTTPException(detail='маалымат жок', status_code=400)

    return super_follow_db


@super_follow_router.put('/{super_follow_id}/', response_model=dict)
async def update_super_follow(follow_id: int, follow: SuperFollowInputSchema,
                             db: Session = Depends(get_db)):

    follow_db = (db.query(SuperFollow).filter(SuperFollow.id == follow_id).first())

    if not follow_db:
        raise HTTPException(detail='Мындай follow жок',status_code=400)

    for follow_key, follow_value in follow.dict().items():
        setattr(follow_db, follow_key, follow_value)

    db.commit()
    db.refresh(follow_db)

    return {'message': 'SuperFollow өзгөртүлдү'}


@super_follow_router.delete('/{super_follow_id}/', response_model=dict)
async def delete_follow(follow_id: int, db: Session = Depends(get_db)):
    follow_db = (db.query(SuperFollow).filter(SuperFollow.id == follow_id).first())

    if not follow_db:
        raise HTTPException(detail='Мындай follow жок', status_code=400)

    db.delete(follow_db)
    db.commit()
    return {'message': 'follow өчүрүлдү'}
