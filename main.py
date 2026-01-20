from fastapi import FastAPI
import uvicorn
from Duolingo.mysite.api import (country, users, follow, super_follow, family_follow, max_follow, language, course,
                                 lesson, exercise, chat, chat_member, message, add_friends, language_progress,
                                 lesson_complete, achievement, auth)
from Duolingo.mysite.admin import setup

duolingo_app = FastAPI(title='Duolingo')

duolingo_app.include_router(country.country_router)
duolingo_app.include_router(users.user_router)
duolingo_app.include_router(follow.follow_router)
duolingo_app.include_router(super_follow.super_follow_router)
duolingo_app.include_router(family_follow.family_follow_router)
duolingo_app.include_router(max_follow.max_follow_router)
duolingo_app.include_router(language.language_router)
duolingo_app.include_router(course.course_router)
duolingo_app.include_router(lesson.lesson_router)
duolingo_app.include_router(exercise.exercise_router)
duolingo_app.include_router(chat.chat_router)
duolingo_app.include_router(chat_member.chat_member_router)
duolingo_app.include_router(message.message_router)
duolingo_app.include_router(add_friends.add_friends_router)
duolingo_app.include_router(language_progress.language_progress_router)
duolingo_app.include_router(lesson_complete.lesson_completion_router)
duolingo_app.include_router(auth.auth_router)
duolingo_app.setup()

if __name__ == '__main__':
    uvicorn.run(duolingo_app, host='127.0.0.1', port=8000)
