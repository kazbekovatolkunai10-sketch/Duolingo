from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from mysite.admin.setup import setup_admin
from mysite.api import (
    follow, language, superFollow, add_friends,
    country, lesson_level, achievement, course, lesson, maxFollow,
    lesson_complete
)

from mysite.api.api_chat.auth import auth_router
from mysite.api.api_chat.user import user_router
from mysite.api.api_chat.group_http import group_http
from mysite.api.api_chat.people_http import people_http
from mysite.api.api_chat.messages_http import messages_http
from mysite.api.api_chat.ws_messages import ws_router
from mysite.api.api_chat.chats_list_http import chats_router
from mysite.api.api_chat.chats_read_http import read_router
from mysite.api.api_chat.dialogs_http import dialogs_router
from mysite.api.api_chat.messages_edit_http import messages_edit_router

duolingo_app = FastAPI(title="Duolingo")

# ✅ Middleware СРАЗУ после создания app
duolingo_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # dev
    allow_credentials=False,      # ✅ важно при "*"
    allow_methods=["*"],
    allow_headers=["*"],
)

setup_admin(duolingo_app)

# API
duolingo_app.include_router(follow.follow_router)
duolingo_app.include_router(superFollow.super_follow_router)
# duolingo_app.include_router(message.message_router)
duolingo_app.include_router(add_friends.add_friends_router)
duolingo_app.include_router(country.country_router)
duolingo_app.include_router(lesson_level.lesson_level_router)
duolingo_app.include_router(achievement.achievement_router)
duolingo_app.include_router(language.language_router)
duolingo_app.include_router(course.course_router)
duolingo_app.include_router(lesson.lesson_router)
duolingo_app.include_router(maxFollow.max_follow_router)
duolingo_app.include_router(lesson_complete.lesson_completion_router)



duolingo_app.include_router(auth_router)
duolingo_app.include_router(user_router)

# HTTP
duolingo_app.include_router(group_http)
duolingo_app.include_router(people_http)
duolingo_app.include_router(messages_http)

# WS (только сообщения)
duolingo_app.include_router(ws_router)

duolingo_app.include_router(chats_router)
duolingo_app.include_router(read_router)

duolingo_app.include_router(dialogs_router)

duolingo_app.include_router(messages_edit_router)


if __name__ == "__main__":
    uvicorn.run(duolingo_app, host="127.0.0.1", port=8001)
