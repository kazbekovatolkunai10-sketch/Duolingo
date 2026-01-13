from fastapi import APIRouter, Depends, HTTPException
from Duolingo.mysite.database.models import Rating
from Duolingo.mysite.database.schema import RatingInputSchema, RatingOutSchema
from Duolingo.mysite.database.db import SessionLocal
from typing import List
from sqlalchemy.orm import Session

rating_router = APIRouter(prefix='/ratings', tags=['Ratings'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@rating_router.post('/', response_model=RatingOutSchema)
async def create_rating(rating: RatingInputSchema, db: Session = Depends(get_db)):
    rating_db = Rating(**rating.dict())
    db.add(rating_db)
    db.commit()
    db.refresh(rating_db)
    return rating_db


@rating_router.get('/', response_model=RatingOutSchema)
async def list_rating(db: Session = Depends(get_db)):
    return db.query(Rating).all()


@rating_router.get('/{rating_id}/', response_model=RatingOutSchema)
async def detail_rating(rating_id: int, db: Session = Depends(get_db)):
    rating_db = db.query(Rating).filter(Rating.id == rating_id).first()
    if not rating_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)

    return rating_db


@rating_router.put('/{rating_id}/', response_model=dict)
async def update_rating(rating_id: int, rating: RatingInputSchema,
                        db: Session = Depends(get_db)):
    rating_db = db.query(Rating).filter(Rating.id == rating_id).first()
    if not rating_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)

    for rating_key, rating_value in rating.dict().items():
        setattr(rating_db, rating_key, rating_value)

    db.commit()
    db.refresh(rating_db)
    return {'massage': 'Успешно изменено'}


@rating_router.delete('/{rating_id}/', response_model=dict)
async def delete_rating(rating_id: int, db: Session = Depends(get_db)):
    rating_db = db.query(Rating).filter(Rating.id == rating_id).first()
    if not rating_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)

    db.delete(rating_db)
    db.commit()
    return {'massage': 'Успешно удалено'}
