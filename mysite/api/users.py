from fastapi import APIRouter, Depends, HTTPException
from Duolingo.mysite.database.models import UserProfile
from Duolingo.mysite.database.schema import (UserProfileInputSchema, UserProfileOutSchema, UserListSchema,
                                             UserProfileListSchema, UserProfileDetailSchema)
from Duolingo.mysite.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List

user_router = APIRouter(prefix='/users', tags=['Users'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@user_router.get('/', response_model=List[UserProfileListSchema])
async def list_user(db: Session = Depends(get_db)):
    users = db.query(UserProfile).all()

    result = []

    for user in users:
        streak = user.user_streak[0].current_streak if user.user_streak else 0

    max_level = max((lvl.level for lvl in user.lesson_user), default=1)

    result.append({'id': user.id, 'avatar': user.avatar, 'first_name': user.first_name,
                   'last_name': user.last_name, 'username': user.username, 'level': max_level, 'streak': streak})

    return result


@user_router.get('/{user_id}', response_model=UserProfileDetailSchema)
async def detail_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserProfile).filter(UserProfile.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    streak = user.user_streak[0].current_streak if user.user_streak else 0

    levels = [{'id': lvl.id, 'course_id': lvl.course_id, 'level': lvl.level,
               'experience': lvl.experience, 'xp_to_next_level': lvl.xp_to_next_level}
        for lvl in user.lesson_user]

    achievements = [{'id': a.achievement_user.id, 'title': a.achievement_user.title}
        for a in user.achievement_user]

    return {'id': user.id, 'avatar': user.avatar, 'first_name': user.first_name,
            'last_name': user.last_name, 'username': user.username, 'streak': streak,
            'levels': levels, 'achievements': achievements}


@user_router.put('/{user_id}/', response_model=dict)
async def update_user(user_id: int, user: UserProfileInputSchema, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.id == user_id).first()

    if not user_db:
        raise HTTPException(status_code=400, detail='Мындай колдонуучу жок')

    for key, value in user.dict().items():
        setattr(user_db, key, value)

    db.commit()
    db.refresh(user_db)

    return {'message': 'Колдонуучу өзгөртүлдү'}


@user_router.delete('/{user_id}/', response_model=dict)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.id == user_id).first()

    if not user_db:
        raise HTTPException(detail='Мындай колдонуучу жок', status_code=400)

    db.delete(user_db)
    db.commit()

    return {'message': 'Колдонуучу өчүрүлдү'}
