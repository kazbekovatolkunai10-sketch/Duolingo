from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from Duolingo.mysite.database.models import LessonCompletion, Lesson, LanguageProgress, UserProfile, Streak
from Duolingo.mysite.database.schema import LessonCompletionInputSchema, CompleteLessonResponseSchema
from Duolingo.mysite.database.db import SessionLocal
from Duolingo.mysite.api.deps import get_current_user
from Duolingo.mysite.api.achievement import give_achievement_if_not_exists
from datetime import date, timedelta

lesson_completion_router = APIRouter(prefix='/lesson_completion', tags=['Lesson Completion'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@lesson_completion_router.post('/lesson_completion/', response_model=CompleteLessonResponseSchema)
async def complete_lesson(lesson_complete: LessonCompletionInputSchema, db: Session = Depends(get_db),
                          user: UserProfile = Depends(get_current_user)):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_complete.lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail='Урок не найден')

    if lesson.is_locked:
        raise HTTPException(status_code=400, detail='Урок заблокирован')

    exists = db.query(LessonCompletion).filter(LessonCompletion.user_id == user.id,LessonCompletion.lesson_id == lesson.id).first()
    if exists:
        raise HTTPException(status_code=400, detail='Урок уже завершён')

    course_id = lesson.course_id
    language_id = lesson.course_lesson.language_id

    if lesson.order > 1:
        prev_lesson = db.query(Lesson).filter(Lesson.course_id == course_id, Lesson.order == lesson.order - 1).first()

        if not prev_lesson:
            raise HTTPException(status_code=400, detail='Предыдущий урок не найден')

        prev_completed = db.query(LessonCompletion).filter(LessonCompletion.user_id == user.id, LessonCompletion.lesson_id == prev_lesson.id).first()

        if not prev_completed:
            raise HTTPException(status_code=400, detail='Сначала пройди предыдущий урок')

    completion = LessonCompletion(user_id=user.id, lesson_id=lesson.id)
    db.add(completion)
    db.flush()

    progress = db.query(LanguageProgress).filter(LanguageProgress.user_id == user.id, LanguageProgress.language_id == language_id).first()

    if not progress:
        progress = LanguageProgress(user_id=user.id, language_id=language_id)
        db.add(progress)
        db.flush()

    progress.add_experience(lesson.xp_reward)

    next_lesson = db.query(Lesson).filter(Lesson.course_id == lesson.course_id, Lesson.order == lesson.order + 1).first()

    if next_lesson:
        next_lesson.is_locked = False
        db.add(next_lesson)

    streak = db.query(Streak).filter(Streak.user_id == user.id).first()

    if not streak:
        streak = Streak(usser_id=user.id, current_streak=0)
        db.add(streak)
        db.flush()

    current_streak = streak.current_streak

    db.commit()
    db.refresh(completion)
    db.refresh(progress)

    return {'completion': {'id': completion.id, 'user_id': completion.user_id, 'lesson_id': completion.lesson_id},
            'level': progress.level, 'experience': progress.experience, 'xp_to_next_level': progress.xp_to_next_level,
            'streak': streak.current_streak}