from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import date, datetime
from .models import RoleChoices, LevelChoices, TypeChoices


class CountryInputSchema(BaseModel):
    country_image: str
    country_name: str


class CountryOutSchema(BaseModel):
    id: int
    country_image: str
    country_name: str


class UserProfileInputSchema(BaseModel):
    avatar: str
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    password: str
    phone_number: Optional[str]
    is_active: bool
    country_id: int


class UserProfileOutSchema(BaseModel):
    id: int
    avatar: str
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    password: str
    phone_number: Optional[str]
    role: RoleChoices
    is_active: bool
    country_id: int
    date_register: datetime


class UserProfileLoginSchema(BaseModel):
    username: str
    password: str


class UserListSchema(BaseModel):
    avatar: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]


class UserProfileListSchema(BaseModel):
    id: int
    avatar: Optional[str]
    first_name: str
    last_name: str
    username: str

    level: int
    streak: int

    class Config:
        from_attributes = True


class LanguageProgressInputSchema(BaseModel):
    language_id: int
    level: int
    experience: int
    max_level: int


class LanguageProgressOutSchema(BaseModel):
    id: int
    language_id: int
    level: int
    experience: int
    xp_to_next_level: int


class AchievementMiniOutSchema(BaseModel):
    id: int
    title: str


class UserProfileDetailSchema(BaseModel):
    id: int
    avatar: Optional[str]
    first_name: str
    last_name: str
    username: str

    streak: int
    levels: List[LanguageProgressOutSchema]
    achievements: List[AchievementMiniOutSchema]

    class Config:
        from_attributes = True


class FollowInputSchema(BaseModel):
    following_id: int
    follower_id: int


class FollowOutSchema(BaseModel):
    id: int
    following_id: int
    follower_id: int


class SuperFollowInputSchema(BaseModel):
    title: str
    description: str


class SuperFollowOutSchema(BaseModel):
    id: int
    title: str
    description: str


class FamilyFollowInputSchema(BaseModel):
    title: str
    description: str


class FamilyFollowOutSchema(BaseModel):
    id: int
    title: str
    description: str


class MaxFollowInputSchema(BaseModel):
    title: str
    description: str


class MaxFollowOutSchema(BaseModel):
    id: int
    title: str
    description: str


class LanguageInputSchema(BaseModel):
    code: str
    name: str
    is_active: bool


class LanguageOutSchema(BaseModel):
    id: int
    code: str
    name: str
    is_active: bool


class CourseInputSchema(BaseModel):
    language_id: int
    title: str
    description: str
    order: int


class CourseOutSchema(BaseModel):
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
    is_locked: bool
    xp_reward: int


class LessonOutSchema(BaseModel):
    id: int
    course_id: int
    title: str
    order: int
    is_locked: bool
    xp_reward: int

    class Config:
        from_attributes = True


class ExerciseInputSchema(BaseModel):
    lesson_id: int
    questions: str
    correct_answer: str


class ExerciseOutSchema(BaseModel):
    id: int
    lesson_id: int
    questions: str
    type: LevelChoices
    correct_answer: str


class OptionInputSchema(BaseModel):
    exercise_id: int


class OptionOutSchema(BaseModel):
    id: int
    exercise_id: int


class UserProgressInputSchema(BaseModel):
    user_id: int
    lesson_id: int
    completed: bool
    score: int


class UserProgressOutSchema(BaseModel):
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


class XPHistoryOutSchema(BaseModel):
    id: int
    user_id: int
    xp: int
    reason: str
    created_date: datetime


class StreakInputSchema(BaseModel):
    user_id: int
    current_streak: int


class StreakOutSchema(BaseModel):
    id: int
    user_id: int
    current_streak: int
    last_activity: date


class ChatInputSchema(BaseModel):
    type: TypeChoices
    language_id: int


class ChatOutSchema(BaseModel):
    id: int
    type: TypeChoices
    language_id: int
    create_at: datetime


class ChatMemberInputSchema(BaseModel):
    chat_id: int
    user_id: int


class ChatMemberOutSchema(BaseModel):
    id: int
    chat_id: int
    user_id: int
    joined_at: datetime


class MessageInputSchema(BaseModel):
    chat_id: int
    sender_id: int
    content: str
    is_read: bool


class MessageOutShema(BaseModel):
    id: int
    chat_id: int
    sender_id: int
    content: str
    is_read: bool
    created_at: datetime


class AddFriendsInputSchema(BaseModel):
    user_id: int


class AddFriendsOutSchema(BaseModel):
    id: int
    user_id: int


class RatingInputSchema(BaseModel):
    user_id: int
    streak_id: int


class RatingOutSchema(BaseModel):
    id: int
    user_id: int
    streak_id: int


class LessonCompletionInputSchema(BaseModel):
    lesson_id: int


class LessonCompletionOutSchema(BaseModel):
    id: int
    user_id: int
    lesson_id: int

    class Config:
        from_attributes = True


class CompleteLessonResponseSchema(BaseModel):
    completion: LessonCompletionOutSchema
    level: int
    experience: int
    xp_to_next_level: int
    streak: int

    class Config:
        from_attributes = True


class AchievementInputSchema(BaseModel):
    lesson_level_id: int


class AchievementOutSchema(BaseModel):
    id: int
    lesson_level_id: int
