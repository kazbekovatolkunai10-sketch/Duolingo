from fastapi import APIRouter, Depends, HTTPException
from Duolingo.mysite.database.models import Chat
from Duolingo.mysite.database.schema import ChatInputSchema, ChatOutSchema
from Duolingo.mysite.database.db import SessionLocal
from typing import List
from sqlalchemy.orm import Session


chat_router = APIRouter(prefix='/chat', tags=['Chat'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@chat_router.post('/', response_model=ChatOutSchema)
async def create_chat(chat: ChatInputSchema, db: Session = Depends(get_db)):
    chat_db = Chat(**chat.dict())
    db.add(chat_db)
    db.commit()
    db.refresh(chat_db)
    return chat_db

@chat_router.get('/', response_model=List[ChatOutSchema])
async def list_chat(db: Session = Depends(get_db)):
    return db.query(Chat).all()

@chat_router.get('/{chat_id}/', response_model=ChatOutSchema)
async def detail_chat(chat_id: int, db: Session = Depends(get_db)):
    chat_db = db.query(Chat).filter(Chat.id == chat_id).first()
    if not chat_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)
    return chat_db

@chat_router.put('/{chat_id}/', response_model=dict)
async def update_chat(chat_id: int, chat: ChatInputSchema, db: Session = Depends(get_db)):
    chat_db = db.query(Chat).filter(Chat.id == chat_id).first()
    if not chat_db:
        raise HTTPException(detail='Мындай option жок', status_code=400)

    for chat_key, chat_value in chat.dict().items():
        setattr(chat_db, chat_key, chat_value)

    db.commit()
    db.refresh(chat_db)
    return {'message': 'Option озгорулду'}


@chat_router.delete('/{chat_id}/', response_model=dict)
async def delete_chat(chat_id: int, db: Session = Depends(get_db)):
    chat_db = db.query(Chat).filter(Chat.id == chat_id).first()
    if not chat_db:
        raise HTTPException(detail='Мындай option жок', status_code=400)
    db.delete(chat_db)
    db.commit()
    return {'message': 'Option удалить болду'}
