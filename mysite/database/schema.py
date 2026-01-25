from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional, List
from datetime import date, datetime

from .models import RoleChoices, LevelChoices, TypeChoices  # TypeChoices можно оставить если используешь где-то ещё


# =========================
# BASE
# =========================
class ORMBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


# =========================
# USER
# =========================
class UserCreateSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str


class UserProfileOutSchema(ORMBase):
    id: int
    avatar: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: str
    email: EmailStr
    phone_number: Optional[str] = None
    role: RoleChoices
    is_active: bool
    date_register: datetime


class UserProfileInputSchema(BaseModel):
    avatar: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None


class UserResponseSchema(BaseModel):
    id: int
    email: EmailStr
    username: str
    date_register: datetime

    class Config:
        from_attributes = True



# если тебе нужно отдавать "короткого пользователя" в списках:
class UserShortOut(ORMBase):
    id: int
    username: str
    email: EmailStr


# =========================
# FOLLOW
# =========================
class FollowInputSchema(BaseModel):
    following_id: int
    follower_id: int


class FollowOutSchema(ORMBase):
    id: int
    following_id: int
    follower_id: int


class SuperFollowInputSchema(BaseModel):
    title: str
    description: str


class SuperFollowOutSchema(ORMBase):
    id: int
    title: str
    description: str


class MaxFollowInputSchema(BaseModel):
    title: str
    description: str


class MaxFollowOutSchema(ORMBase):
    id: int
    title: str
    description: str



# =========================
# LANGUAGE / COURSE / LESSON / ...
# (твои duolingo-схемы можно оставить почти без изменений)
# =========================
class LanguageInputSchema(BaseModel):
    code: str
    name: str
    is_active: bool


class LanguageOutSchema(ORMBase):
    id: int
    code: str
    name: str
    is_active: bool


class CourseInputSchema(BaseModel):
    language_id: int
    title: str
    description: str
    order: int


class CourseOutSchema(ORMBase):
    id: int
    language_id: int
    title: str
    description: str
    level: LevelChoices
    order: int


class LessonInputSchema(BaseModel):
    course_id: int
    title: str
    order: int
    is_locked: bool = False
    xp_reward: int = 10


class LessonOutSchema(ORMBase):
    id: int
    course_id: int
    title: str
    order: int
    is_locked: bool
    xp_reward: int


class ExerciseInputSchema(BaseModel):
    lesson_id: int
    questions: str
    correct_answer: str
    type: LevelChoices


class ExerciseOutSchema(ORMBase):
    id: int
    lesson_id: int
    questions: str
    type: LevelChoices
    correct_answer: str


class OptionInputSchema(BaseModel):
    exercise_id: int


class OptionOutSchema(ORMBase):
    id: int
    exercise_id: int


class UserProgressInputSchema(BaseModel):
    user_id: int
    lesson_id: int
    completed: bool = False
    score: int = 0


class UserProgressOutSchema(ORMBase):
    id: int
    user_id: int
    lesson_id: int
    completed: bool
    score: int
    xp_earned: int
    completed_date: datetime


class XPHistoryInputSchema(BaseModel):
    user_id: int
    xp: int
    reason: str


class XPHistoryOutSchema(ORMBase):
    id: int
    user_id: int
    xp: int
    reason: str
    created_date: datetime


class StreakOutSchema(ORMBase):
    id: int
    user_id: int
    current_steak: int
    last_activity: date


class AddFriendsInputSchema(BaseModel):
    user_id: int


class AddFriendsOutSchema(ORMBase):
    id: int
    user_id: int


class CountryInputSchema(BaseModel):
    user_id: int


class CountryOutSchema(ORMBase):
    id: int
    user_id: int


class RatingInputSchema(BaseModel):
    user_id: int
    streak_id: int


class RatingOutSchema(ORMBase):
    id: int
    user_id: int
    streak_id: int


class LessonLevelInputSchema(BaseModel):
    user_id: int
    lesson_id: int
    level: int = 1
    experience: int = 0
    max_level: int = 100


class LessonLevelOutSchema(ORMBase):
    id: int
    user_id: int
    lesson_id: int
    level: int
    experience: int
    max_level: int


class LessonCompletionInputSchema(BaseModel):
    lesson_id: int


class LessonCompletionOutSchema(ORMBase):
    id: int
    user_id: int
    lesson_id: int
    date_completed: datetime


class AchievementInputSchema(BaseModel):
    title: str
    code: str


class AchievementOutSchema(ORMBase):
    id: int
    title: str
    code: str


# =========================
# CHAT (НОВАЯ ВЕРСИЯ) — под твои модели:
# ChatGroup / GroupPeople / ChatMessage / ChatReadState
# =========================
class GroupCreateIn(BaseModel):
    title: str
    is_private: bool = False


class GroupOut(ORMBase):
    id: int
    owner_id: int
    title: str
    create_date: datetime
    is_private: bool


class AddMembersIn(BaseModel):
    user_ids: List[int]


class GroupMemberOut(ORMBase):
    id: int
    group_id: int
    user_id: int
    joined_date: date
    user: UserShortOut


class GroupDetailOut(ORMBase):
    id: int
    owner_id: int
    title: str
    create_date: datetime
    is_private: bool
    members: List[GroupMemberOut] = []


class MessageCreateIn(BaseModel):
    group_id: int
    text: str


class MessageOut(ORMBase):
    id: int
    group_id: int
    user_id: int
    text: str
    created_date: datetime
    is_deleted: bool
    edited_at: Optional[datetime] = None


class MessagesPageOut(BaseModel):
    group_id: int
    items: List[MessageOut]
    has_more: bool
    before_id: Optional[int] = None


class LastMessageOut(ORMBase):
    id: int
    user_id: int
    text: str
    created_date: datetime


class ChatListItemOut(BaseModel):
    group_id: int
    title: Optional[str] = None
    is_private: bool
    members_count: int
    last_message: Optional[LastMessageOut] = None
    unread_count: int


class ReadStateOut(ORMBase):
    id: int
    group_id: int
    user_id: int
    last_read_message_id: Optional[int] = None
    updated_at: datetime


# =========================
# TOKENS
# =========================
class TokenPairOut(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
