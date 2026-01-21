from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import date, datetime
from .models import RoleChoices, LevelChoices, TypeChoices


class ORMBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class UserProfileInputSchema(BaseModel):
    avatar: Optional[str] = None
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    password: str
    phone_number: Optional[str] = None
    is_active: bool = False


class UserProfileOutSchema(ORMBase):
    id: int
    avatar: Optional[str] = None
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    password: str
    phone_number: Optional[str] = None
    role: RoleChoices
    is_active: bool
    date_register: datetime


class UserProfileLoginSchema(BaseModel):
    username: str
    password: str


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


class FamilyFollowInputSchema(BaseModel):
    title: str
    description: str


class FamilyFollowOutSchema(ORMBase):
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


class StreakInputSchema(BaseModel):
    user_id: int
    current_streak: int


class StreakOutSchema(ORMBase):
    id: int
    user_id: int
    current_streak: int
    last_activity: date


class ChatInputSchema(BaseModel):
    type: TypeChoices
    language_id: int


class ChatOutSchema(ORMBase):
    id: int
    type: TypeChoices
    language_id: int
    create_at: datetime


class ChatMemberInputSchema(BaseModel):
    chat_id: int
    user_id: int


class ChatMemberOutSchema(ORMBase):
    id: int
    chat_id: int
    user_id: int
    joined_at: datetime


class MessageInputSchema(BaseModel):
    chat_id: int
    sender_id: int
    content: str
    is_read: bool = False


class MessageOutShema(ORMBase):
    id: int
    chat_id: int
    sender_id: int
    content: str
    is_read: bool
    created_at: datetime


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
