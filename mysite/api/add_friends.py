from fastapi import APIRouter, Depends, HTTPException
from Duolingo.mysite.database.models import AddFriends
from Duolingo.mysite.database.schema import AddFriendsInputSchema, AddFriendsOutSchema
from Duolingo.mysite.database.db import SessionLocal
from typing import List
from sqlalchemy.orm import Session

add_friends_router = APIRouter(prefix='add_friends', tags=['Add Friends'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@add_friends_router.post('/', response_model=AddFriendsOutSchema)
async def create_add_friend(add_friend: AddFriendsInputSchema, db: Session = Depends(get_db)):
    add_friend_db = AddFriends(**add_friend.dict())
    db.add(add_friend_db)
    db.commit()
    db.refresh(add_friend_db)
    return add_friend_db


@add_friends_router.get('/', response_model=AddFriendsOutSchema)
async def list_add_friend(db: Session = Depends(get_db)):
    return db.query(AddFriends).all()


@add_friends_router.get('/{add_friend_id}/', response_model=AddFriendsOutSchema)
async def detail_add_friend(add_friend_id: int, db: Session = Depends(get_db)):
    add_friend_db = db.query(AddFriends).filter(AddFriends.id == add_friend_id).first()
    if not add_friend_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)

    return add_friend_db


@add_friends_router.put('/{add_friend_id}/', response_model=dict)
async def update_add_friend(add_friend_id: int, add_friend: AddFriendsInputSchema,
                            db: Session = Depends(get_db)):
    add_friend_db = db.query(AddFriends).filter(AddFriends.id == add_friend_id).first()
    if not add_friend_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)

    for add_friend_key, add_friend_value in add_friend.dict().items():
        setattr(add_friend_db, add_friend_key, add_friend_value)
    db.commit()
    db.refresh(add_friend_db)
    return {'massage': 'Успешно изменено'}


@add_friends_router.delete('/{add_friend_id}/', response_model=dict)
async def delete_add_friend(add_friend_id: int, db: Session = Depends(get_db)):
    add_friend_db = db.query(AddFriends).filter(AddFriends.id == add_friend_id).first()
    if not add_friend_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)

    db.delete(add_friend_db)
    db.commit()
    return {'massage': 'Успешно удалено'}
