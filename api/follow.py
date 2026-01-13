from fastapi import APIRouter, Depends, HTTPException
from mysite.database.models import Follow
from mysite.database.schema import FollowOutSchema, FollowInputSchema
from mysite.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List


follow_router = APIRouter(prefix='/follow', tags=['Follow CRUD'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@follow_router.post("/", response_model=FollowOutSchema)
def create_follow(
    follow: FollowInputSchema, db: Session = Depends(get_db)):

    follow = Follow(**follow.dict())
    db.add(follow)
    db.commit()
    db.refresh(follow)
    return follow

@follow_router.get('/', response_model=List[FollowOutSchema])
async def list_user(db: Session = Depends(get_db)):
    return db.query(Follow).all()


@follow_router.get('/{follow_id}/', response_model=FollowOutSchema)
async def detail_user(follow_id: int, db: Session = Depends(get_db), follow_db=None):
    follow_id = db.query(Follow).filter(Follow.id == follow_id).first()

    if not follow_db:
        raise HTTPException(detail='маалымат жок', status_code=400)

    return follow_db

@follow_router.put('/{follow_id}/', response_model=dict)
async def update_follow(follow_id: int, follow: FollowInputSchema,
    db: Session = Depends(get_db)):

    follow.db = (db.query(Follow).filter(Follow.id == follow_id).first())

    if not follow.db:
        raise HTTPException(detail='Мындай follow жок',status_code=400)

    for follow_key, follow_value in follow.dict().items():
        setattr(follow.db, follow_key, follow_value)

    db.commit()
    db.refresh(follow.db)

    return {'message': 'follow өзгөртүлдү'}


@follow_router.delete('/{follow_id}/', response_model=dict)
async def delete_follow(follow_id: int, db: Session = Depends(get_db)):
    follow_db = (db.query(Follow).filter(Follow.id == follow_id).first())

    if not follow_db:
        raise HTTPException(detail='Мындай follow жок', status_code=400)

    db.delete(follow_db)
    db.commit()
    return {'message': 'follow өчүрүлдү'}