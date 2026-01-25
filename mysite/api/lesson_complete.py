from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from mysite.database.models import LessonCompletion, Lesson, LessonLevel, UserProfile, Streak
from mysite.database.schema import LessonCompletionInputSchema, LessonCompletionOutSchema
from mysite.database.db import SessionLocal
from mysite.api.api_chat.deps import get_current_user
from mysite.api.achievement import give_achievement_if_not_exists
from datetime import date

lesson_completion_router = APIRouter(prefix='/lesson_completion', tags=['Lesson Completion'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@lesson_completion_router.post('/', response_model=LessonCompletionOutSchema)
async def complete_lesson(lesson_complete: LessonCompletionInputSchema, user: UserProfile = Depends(get_current_user),
    db: Session = Depends(get_db)):
    lesson_id = lesson_complete.lesson_id

    completed = db.query(LessonCompletion).filter(
        LessonCompletion.user_id == user.id,
        LessonCompletion.lesson_id == lesson_id).first()

    if completed:
        raise HTTPException(status_code=400, detail='Урок уже завершён')

    lesson = db.query(Lesson).filter(
        Lesson.id == lesson_id).first()

    if not lesson:
        raise HTTPException(status_code=400, detail='Урок не найден')

    completion = LessonCompletion(
        user_id=user.id,
        lesson_id=lesson_id)
    db.add(completion)

    lesson_level = db.query(LessonLevel).filter(
        LessonLevel.user_id == user.id,
        LessonLevel.lesson_id == lesson_id).first()

    if not lesson_level:
        lesson_level = LessonLevel(
            user_id=user.id,
            lesson_id=lesson_id
        )
        db.add(lesson_level)

    lesson_level.add_experience(lesson.xp_reward)

    streak = db.query(Streak).filter(
        Streak.user_id == user.id
    ).first()

    if not streak:
        streak = Streak(
            user_id=user.id,
            current_streak=0,
            last_activity=date.today()
        )
        db.add(streak)

    streak.update_after_lesson()

    next_lesson = db.query(Lesson).filter(
        Lesson.course_id == lesson.course_id,
        Lesson.order > lesson.order
    ).order_by(
        Lesson.order.asc()
    ).first()

    if next_lesson:
        next_lesson.is_locked = False

    give_achievement_if_not_exists(db, user.id, 'first_lesson')

    db.commit()
    db.refresh(completion)

    return completion
