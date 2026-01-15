from fastapi import APIRouter, Depends, HTTPException
from Duolingo.mysite.database.models import Lesson
from Duolingo.mysite.database.schema import LessonInputSchema, LessonOutSchema
from Duolingo.mysite.database.db import SessionLocal
from typing import List
from sqlalchemy.orm import Session

lesson_router = APIRouter(prefix='/lesson', tags=['Lesson'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@lesson_router.post('/', response_model=LessonOutSchema)
async def create_lesson(lesson: LessonInputSchema, db: Session = Depends(get_db)):
    lesson_db = Lesson(**lesson.dict())
    db.add(lesson_db)
    db.commit()
    db.refresh(lesson_db)
    return lesson_db


@lesson_router.get('/', response_model=List[LessonOutSchema])
async def list_lesson(db: Session = Depends(get_db)):
    return db.query(Lesson).all()


@lesson_router.get('/{lesson_id}/', response_model=LessonOutSchema)
async def detail_lesson(lesson_id: int, db: Session = Depends(get_db)):
    lesson_db = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)

    return lesson_db


@lesson_router.put('/{lesson_id}/', response_model=dict)
async def update_lesson(lesson_id: int, lesson: LessonInputSchema,
                             db: Session = Depends(get_db)):
    lesson_db = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)

    for lesson_key, lesson_value in lesson.dict().items():
        setattr(lesson_db, lesson_key, lesson_value)

    db.commit()
    db.refresh(lesson_db)
    return {'message': 'Успешно изменено'}


@lesson_router.delete('/{lesson_id}/', response_model=dict)
async def delete_lesson(lesson_id: int, db: Session = Depends(get_db)):
    lesson_db = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)

    db.delete(lesson_db)
    db.commit()
    return {'message': 'Успешно удалено'}