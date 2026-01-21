from fastapi import APIRouter, Depends, HTTPException
from mysite.database.models import Exercise
from mysite.database.schema import ExerciseInputSchema, ExerciseOutSchema
from mysite.database.db import SessionLocal
from typing import List
from sqlalchemy.orm import Session

exercise_router = APIRouter(prefix='/exercise', tags=['Exercise'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@exercise_router.post('/', response_model=ExerciseOutSchema)
async def create_exercise(exercise: ExerciseInputSchema, db: Session = Depends(get_db)):
    exercise_db = Exercise(**exercise.dict())
    db.add(exercise_db)
    db.commit()
    db.refresh(exercise_db)
    return exercise_db


@exercise_router.get('/', response_model=List[ExerciseOutSchema])
async def list_exercise(db: Session = Depends(get_db)):
    return db.query(Exercise).all()


@exercise_router.get('/{exercise_id}/', response_model=ExerciseOutSchema)
async def detail_exercise(exercise_id: int, db: Session = Depends(get_db)):
    exercise_db = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not exercise_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)
    return exercise_db


@exercise_router.put('/{exercise_id}/', response_model=dict)
async def update_exercise(exercise_id: int, exercise: ExerciseInputSchema,
                          db: Session = Depends(get_db)):
    exercise_db = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not exercise_db:
        raise HTTPException(detail='Мындай exercise жок', status_code=400)

    for exercise_key, exercise_value in exercise.dict().items():
        setattr(exercise_db, exercise_key, exercise_value)

    db.commit()
    db.refresh(exercise_db)
    return {'message': 'Exercise озгорулду'}


@exercise_router.delete('/{exercise_id}/', response_model=dict)
async def delete_exercise(exercise_id: int, db: Session = Depends(get_db)):
    exercise_db = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not exercise_db:
        raise HTTPException(detail='Мындай exercise жок', status_code=400)

    db.delete(exercise_db)
    db.commit()
    return {'message': 'Exercise удалить болду'}