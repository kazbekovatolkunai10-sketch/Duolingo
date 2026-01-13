from fastapi import FastAPI
import uvicorn
from Duolingo.mysite.api import (users, follow, language, superFollow, chat_member, message, add_friends,
                                 country, rating, lesson_level, achievement, familyFollow, maxFollow,
                                 user_progress, history, auth)


duolingo_app = FastAPI(title='Duolingo')

duolingo_app.include_router(users.user_router)
duolingo_app.include_router(follow.follow_router)
duolingo_app.include_router(superFollow.super_follow_router)
duolingo_app.include_router(chat_member.chat_member_router)
duolingo_app.include_router(message.message_router)
duolingo_app.include_router(add_friends.add_friends_router)
duolingo_app.include_router(country.country_router)
duolingo_app.include_router(rating.rating_router)
duolingo_app.include_router(lesson_level.lesson_level_router)
duolingo_app.include_router(achievement.achievement_router)
duolingo_app.include_router(familyFollow.familyFollow_router)
duolingo_app.include_router(maxFollow.MaxFollow_router)
duolingo_app.include_router(user_progress.user_progress_router)
duolingo_app.include_router(history.history_router)
duolingo_app.include_router(auth.auth_router)

if __name__ == '__main__':
    uvicorn.run(duolingo_app, host='127.0.0.1', port=8000)
