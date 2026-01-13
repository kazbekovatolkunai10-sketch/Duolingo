from fastapi import APIRouter, Depends, HTTPException
from mysite.database.models import LessonLevel
from mysite.database.schema import LessonLevelInputSchema, LessonLevelOutSchema
from mysite.database.db import SessionLocal
from typing import List
from sqlalchemy.orm import Session

lesson_level_router = APIRouter(prefix='/lesson_levels', tags=['Lesson Levels'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@lesson_level_router.post('/', response_model=LessonLevelOutSchema)
async def create_lesson_level(lesson_level: LessonLevelInputSchema, db: Session = Depends(get_db)):
    lesson_level_db = LessonLevel(**lesson_level.dict())
    db.add(lesson_level_db)
    db.commit()
    db.refresh(lesson_level_db)
    return lesson_level_db


@lesson_level_router.get('/', response_model=List[LessonLevelOutSchema])
async def list_lesson_level(db: Session = Depends(get_db)):
    return db.query(LessonLevel).all()


@lesson_level_router.get('/{lesson_level_id}/', response_model=LessonLevelOutSchema)
async def detail_lesson_level(lesson_level_id: int, db: Session = Depends(get_db)):
    lesson_level_db = db.query(LessonLevel).filter(LessonLevel.id == lesson_level_id).first()
    if not lesson_level_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)

    return lesson_level_db


@lesson_level_router.put('/{lesson_level_id}/', response_model=dict)
async def update_lesson_level(lesson_level_id: int, lesson_level: LessonLevelInputSchema,
                              db: Session = Depends(get_db)):
    lesson_level_db = db.query(LessonLevel).filter(LessonLevel.id == lesson_level_id).first()
    if not lesson_level_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)

    for lesson_level_key, lesson_level_value in lesson_level.dict().items():
        setattr(lesson_level_db, lesson_level_key, lesson_level_value)

    db.commit()
    db.refresh(lesson_level_db)
    return {'massage': 'Успешно изменено'}


@lesson_level_router.delete('/{lesson_level_id}/', response_model=dict)
async def delete_lesson_level(lesson_level_id: int, db: Session = Depends(get_db)):
    lesson_level_db = db.query(LessonLevel).filter(LessonLevel.id == lesson_level_id).first()
    if not lesson_level_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)

    db.delete(lesson_level_db)
    db.commit()
    return {'message': 'Успешно удалено'}
