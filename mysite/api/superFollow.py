from fastapi import APIRouter, Depends, HTTPException
from Duolingo.mysite.database.models import SuperFollow
from Duolingo.mysite.database.models import SuperFollowOutSchema, SuperFollowInputSchema
from Duolingo.mysite.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List

super_follow_router = APIRouter(prefix='/super_follow', tags=['super_follow CRUD'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@super_follow_router.post("/", response_model=SuperFollowOutSchema)
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
async def detail_user(follow_id: int, db: Session = Depends(get_db), follow_db=None):
    follow_id = db.query(Follow).filter(Follow.id == follow_id).first()

    if not follow_db:
        raise HTTPException(detail='маалымат жок', status_code=400)

    return follow_db

