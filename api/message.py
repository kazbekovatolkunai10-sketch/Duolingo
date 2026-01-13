from fastapi import APIRouter, Depends, HTTPException
from mysite.database.models import Message
from mysite.database.schema import MessageInputSchema, MessageOutShema
from mysite.database.db import SessionLocal
from sqlalchemy.orm import Session

message_router = APIRouter(prefix='/message', tags=['Messages'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@message_router.post('/', response_model=MessageOutShema)
async def create_message(message: MessageInputSchema, db: Session = Depends(get_db)):
    message_db = Message(**message.dict())
    db.add(message_db)
    db.commit()
    db.refresh(message_db)
    return message_db


@message_router.get('/', response_model=MessageOutShema)
async def list_message(db: Session = Depends(get_db)):
    return db.query(Message).all()


@message_router.get('/{message_id}/', response_model=MessageOutShema)
async def detail_message(message_id: int, db: Session = Depends(get_db)):
    message_db = db.query(Message).filter(Message.id == message_id).first()
    if not message_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)

    return message_db


@message_router.put('/{message_id}/', response_model=dict)
async def update_message(message_id: int, message: MessageInputSchema,
                         db: Session = Depends(get_db)):
    message_db = db.query(Message).filter(Message.id == message_id).first()
    if not message_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)

    for message_key, message_value in message.dict().items():
        setattr(message_db, message_key, message_value)
    db.commit()
    db.refresh(message_db)
    return {'massage': 'Успешно изменено'}


@message_router.delete('/{message_id}/', response_model=dict)
async def delete_message(message_id: int, db: Session = Depends(get_db)):
    message_db = db.query(Message).filter(Message.id == message_id).first()
    if not message_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)

    db.delete(message_db)
    db.commit()
    return {'massage': 'Успешно удалено'}
