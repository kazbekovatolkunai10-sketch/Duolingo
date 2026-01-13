from fastapi import FastAPI
import uvicorn
from Duolingo.mysite.api import (users, follow, language, superFollow, message, add_friends,
                                 country, rating, lesson_level, achievement)

duolingo_app = FastAPI(title='Duolingo')

duolingo_app.include_router(users.user_router)
duolingo_app.include_router(follow.follow_router)
duolingo_app.include_router(superFollow.super_follow_router)
duolingo_app.include_router(message.message_router)
duolingo_app.include_router(add_friends.add_friends_router)
duolingo_app.include_router(country.country_router)
duolingo_app.include_router(rating.rating_router)
duolingo_app.include_router(lesson_level.lesson_level_router)
duolingo_app.include_router(achievement.achievement_router)

if __name__ == '__main__':
    uvicorn.run(duolingo_app, host='127.0.0.1', port=8000)
