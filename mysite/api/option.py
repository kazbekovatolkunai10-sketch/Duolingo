from fastapi import APIRouter, Depends, HTTPException
from Duolingo.mysite.database.models import Option
from Duolingo.mysite.database.schema import OptionInputSchema, OptionOutSchema
from Duolingo.mysite.database.db import SessionLocal
from typing import List
from sqlalchemy.orm import Session


option_router = APIRouter(prefix='/option', tags=['Option'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@option_router.post('/', response_model=OptionOutSchema)
async def create_option(option: OptionInputSchema, db: Session = Depends(get_db)):
    option_db = Option(**option.dict())
    db.add(option_db)
    db.commit()
    db.refresh(option_db)
    return option_db


@option_router.get('/', response_model=List[OptionOutSchema])
async def list_option(db: Session = Depends(get_db)):
    return db.query(Option).all()


@option_router.get('/{option_id}/', response_model=OptionOutSchema)
async def detail_option(option_id: int, db: Session = Depends(get_db)):
    option_db = db.query(Option).filter(Option.id == option_id).first()
    if not option_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)
    return option_db


@option_router.put('/{option_id}/', response_model=dict)
async def update_option(option_id: int, option: OptionInputSchema, db: Session = Depends(get_db)):
    option_db = db.query(Option).filter(Option.id == option_id).first()
    if not option_db:
        raise HTTPException(detail='Мындай option жок', status_code=400)

    for option_key, option_value in option.dict().items():
        setattr(option_db, option_key, option_value)

    db.commit()
    db.refresh(option_db)
    return {'message': 'Option озгорулду'}


@option_router.delete('/{option_id}/', response_model=dict)
async def delete_option(option_id: int, db: Session = Depends(get_db)):
    option_db = db.query(Option).filter(Option.id == option_id).first()
    if not option_db:
        raise HTTPException(detail='Мындай option жок', status_code=400)

    db.delete(option_db)
    db.commit()
    return {'message': 'Option удалить болду'}