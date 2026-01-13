from fastapi import APIRouter, Depends, HTTPException
from Duolingo.mysite.database.models import ChatMember
from Duolingo.mysite.database.schema import ChatMemberInputSchema, ChatMemberOutSchema
from Duolingo.mysite.database.db import SessionLocal
from typing import List
from sqlalchemy.orm import Session

chat_member_router = APIRouter(prefix='/chat_members', tags=['Chat Members'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@chat_member_router.post('/', response_model=ChatMemberOutSchema)
async def create_chat_member(chat_member: ChatMemberInputSchema, db: Session = Depends(get_db)):
    chat_member_db = ChatMember(**chat_member.dict())
    db.add(chat_member_db)
    db.commit()
    db.refresh(chat_member_db)
    return chat_member_db


@chat_member_router.get('/', response_model=List[ChatMemberOutSchema])
async def list_chat_member(db: Session = Depends(get_db)):
    return db.query(ChatMember).all()


@chat_member_router.get('/{chat_member_id}/', response_model=ChatMemberOutSchema)
async def detail_chat_member(chat_member_id: int, db: Session = Depends(get_db)):
    chat_member_db = db.query(ChatMember).filter(ChatMember.id == chat_member_id).first()
    if not chat_member_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)

    return chat_member_db


@chat_member_router.put('/{chat_member_id}/', response_model=dict)
async def update_chat_member(chat_member_id: int, chat_member: ChatMemberInputSchema,
                             db: Session = Depends(get_db)):
    chat_member_db = db.query(ChatMember).filter(ChatMember.id == chat_member_id).first()
    if not chat_member_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)

    for chat_member_key, chat_member_value in chat_member.dict().items():
        setattr(chat_member_db, chat_member_key, chat_member_value)

    db.commit()
    db.refresh(chat_member_db)
    return {'message': 'Успешно изменено'}


@chat_member_router.delete('/{chat_member_id}/', response_model=dict)
async def delete_chet_member(chat_member_id: int, db: Session = Depends(get_db)):
    chat_member_db = db.query(ChatMember).filter(ChatMember.id == chat_member_id).first()
    if not chat_member_db:
        raise HTTPException(detail='Мандый маалымат жок', status_code=400)

    db.delete(chat_member_db)
    db.commit()
    return {'message': 'Успешно удалено'}
