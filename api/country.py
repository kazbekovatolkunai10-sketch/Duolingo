from fastapi import APIRouter, Depends, HTTPException
from mysite.database.models import Country
from mysite.database.schema import CountryInputSchema, CountryOutSchema
from mysite.database.db import SessionLocal
from sqlalchemy.orm import Session

country_router = APIRouter(prefix='countries', tags=['Countries'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@country_router.post('/', response_model=CountryOutSchema)
async def create_country(country: CountryInputSchema, db: Session = Depends(get_db)):
    country_db = Country(**country.dict())
    db.add(country_db)
    db.commit()
    db.refresh(country_db)
    return country_db


@country_router.get('/', response_model=CountryOutSchema)
async def list_country(db: Session = Depends(get_db)):
    return db.query(Country).all()


@country_router.get('/{country_id}/', response_model=CountryOutSchema)
async def detail_country(country_id: int, db: Session = Depends(get_db)):
    country_db = db.query(Country).filter(Country.id == country_id).first()
    if not country_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)

    return country_db


@country_router.put('/{country_id}/', response_model=dict)
async def update_country(country_id: int, country: CountryInputSchema,
                         db: Session = Depends(get_db)):
    country_db = db.query(Country).filter(Country.id == country_id).first()
    if not country_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)

    for country_key, country_value in country.dict().items():
        setattr(country_db, country_key, country_value)

    db.commit()
    db.refresh(country_db)
    return {'massage': 'Успешно изменено'}


@country_router.delete('/{country_id}/', response_model=dict)
async def delete_country(country_id: int, db: Session = Depends(get_db)):
    country_db = db.query(Country).filter(Country.id == country_id).first()
    if not country_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)

    db.delete(country_db)
    db.commit()
    return {'massage': 'Успешно удалено'}
