from .db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    Integer, String, ForeignKey, DateTime, Date, Boolean, Text,
    Enum, UniqueConstraint, Index
)
from datetime import date, datetime, timedelta
from typing import List, Optional
from enum import Enum as PyEnum
from passlib.context import CryptContext


# =========================
# ENUMS
# =========================
class RoleChoices(str, PyEnum):
    user = "user"
    admin = "admin"


class LevelChoices(str, PyEnum):
    A1 = "A1"
    A2 = "A2"
    B1 = "B1"
    B2 = "B2"
    C1 = "C1"
    C2 = "C2"


class TypeChoices(str, PyEnum):
    private = "private"
    group = "group"


pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


# =========================
# USER
# =========================
class UserProfile(Base):
    __tablename__ = "profile"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    avatar: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    first_name: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(String(60), nullable=True)

    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)

    password: Mapped[str] = mapped_column(String, nullable=False)
    phone_number: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    role: Mapped[RoleChoices] = mapped_column(Enum(RoleChoices), default=RoleChoices.user)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)

    date_register: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)

    # -------- duolingo relations --------
    following_user: Mapped[List["Follow"]] = relationship(
        back_populates="following",
        cascade="all, delete-orphan",
        foreign_keys="Follow.following_id",
    )
    follower_user: Mapped[List["Follow"]] = relationship(
        back_populates="follower",
        cascade="all, delete-orphan",
        foreign_keys="Follow.follower_id",
    )

    user_progress: Mapped[List["UserProgres"]] = relationship(
        back_populates="progress_user",
        cascade="all, delete-orphan",
    )
    lesson_user: Mapped[List["LessonLevel"]] = relationship(
        back_populates="user_lesson",
        cascade="all, delete-orphan",
    )
    history_user: Mapped[List["XPHistory"]] = relationship(
        back_populates="user_history",
        cascade="all, delete-orphan",
    )
    user_streak: Mapped[List["Streak"]] = relationship(
        back_populates="streak_user",
        cascade="all, delete-orphan",
    )
    user_add: Mapped[List["AddFriends"]] = relationship(
        back_populates="add_user",
        cascade="all, delete-orphan",
    )
    country_user: Mapped[List["Country"]] = relationship(
        back_populates="user_country",
        cascade="all, delete-orphan",
    )
    rating_user: Mapped[List["Rating"]] = relationship(
        back_populates="user_rating",
        cascade="all, delete-orphan",
    )
    achievement_user: Mapped[List["UserAchievement"]] = relationship(
        back_populates="user_achievement",
        cascade="all, delete-orphan",
    )
    complete_user: Mapped[List["LessonCompletion"]] = relationship(
        back_populates="user_complete",
        cascade="all, delete-orphan",
    )

    # -------- chat relations --------
    owner_group: Mapped[List["ChatGroup"]] = relationship(
        back_populates="owner",
        cascade="all, delete-orphan",
    )
    user_group: Mapped[List["GroupPeople"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )
    user_sms: Mapped[List["ChatMessage"]] = relationship(
        back_populates="user_message",
        cascade="all, delete-orphan",
    )
    refresh_tokens: Mapped[List["RefreshToken"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )

    # -------- password helpers --------
    def set_password(self, raw_password: str) -> None:
        self.password = pwd_context.hash(raw_password)

    def check_password(self, raw_password: str) -> bool:
        return pwd_context.verify(raw_password, self.password)

    def __repr__(self):
        return f"{self.username}"


# =========================
# AUTH TOKENS
# =========================
class RefreshToken(Base):
    __tablename__ = "refresh_token"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    token: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("profile.id"), nullable=False, index=True)
    user: Mapped["UserProfile"] = relationship("UserProfile", back_populates="refresh_tokens")


# =========================
# FOLLOW
# =========================
class Follow(Base):
    __tablename__ = "follow"
    __table_args__ = (
        UniqueConstraint("following_id", "follower_id", name="uq_follow_pair"),
        Index("ix_follow_following_follower", "following_id", "follower_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    following_id: Mapped[int] = mapped_column(ForeignKey("profile.id"), index=True)
    follower_id: Mapped[int] = mapped_column(ForeignKey("profile.id"), index=True)

    following: Mapped["UserProfile"] = relationship(
        back_populates="following_user",
        foreign_keys=[following_id],
    )
    follower: Mapped["UserProfile"] = relationship(
        back_populates="follower_user",
        foreign_keys=[follower_id],
    )


class SuperFollow(Base):
    __tablename__ = "super_follow"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(Text)


class FamilyFollow(Base):
    __tablename__ = "family_follow"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(Text)


class MaxFollow(Base):
    __tablename__ = "max_follow"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(Text)


# =========================
# LANGUAGE / COURSE / LESSON
# =========================
class Language(Base):
    __tablename__ = "language"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String, unique=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    course_language: Mapped[List["Course"]] = relationship(
        back_populates="language",
        cascade="all, delete-orphan",
    )
    # ⚠️ УБРАЛ chat_language — потому что класса Chat у тебя нет. Если надо — привяжем к ChatGroup отдельно.


class Course(Base):
    __tablename__ = "course"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    language_id: Mapped[int] = mapped_column(ForeignKey("language.id"), index=True)

    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(Text)
    level: Mapped[LevelChoices] = mapped_column(Enum(LevelChoices), default=LevelChoices.A1)
    order: Mapped[int] = mapped_column(Integer)

    language: Mapped["Language"] = relationship(back_populates="course_language")
    lesson_course: Mapped[List["Lesson"]] = relationship(
        back_populates="course_lesson",
        cascade="all, delete-orphan",
    )


class Lesson(Base):
    __tablename__ = "lesson"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("course.id"), index=True)

    title: Mapped[str] = mapped_column(String)
    order: Mapped[int] = mapped_column(Integer)

    is_locked: Mapped[bool] = mapped_column(Boolean, default=False)
    xp_reward: Mapped[int] = mapped_column(Integer, default=10)

    course_lesson: Mapped["Course"] = relationship(back_populates="lesson_course")
    exercise_lesson: Mapped[List["Exercise"]] = relationship(
        back_populates="lesson",
        cascade="all, delete-orphan",
    )
    progress_lesson: Mapped[List["UserProgres"]] = relationship(
        back_populates="lesson_progress",
        cascade="all, delete-orphan",
    )
    lesson_level: Mapped[List["LessonLevel"]] = relationship(
        back_populates="lesson",
        cascade="all, delete-orphan",
    )
    complete_lesson: Mapped[List["LessonCompletion"]] = relationship(
        back_populates="lesson_complete",
        cascade="all, delete-orphan",
    )


class Exercise(Base):
    __tablename__ = "exercise"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    lesson_id: Mapped[int] = mapped_column(ForeignKey("lesson.id"), index=True)

    type: Mapped[LevelChoices] = mapped_column(Enum(LevelChoices))
    questions: Mapped[str] = mapped_column(Text)
    correct_answer: Mapped[str] = mapped_column(String)

    lesson: Mapped["Lesson"] = relationship(back_populates="exercise_lesson")
    option: Mapped[List["Option"]] = relationship(
        back_populates="exercise",
        cascade="all, delete-orphan",
    )


class Option(Base):
    __tablename__ = "option"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    exercise_id: Mapped[int] = mapped_column(ForeignKey("exercise.id"), index=True)

    exercise: Mapped["Exercise"] = relationship(back_populates="option")


# =========================
# PROGRESS / HISTORY / STREAK
# =========================
class UserProgres(Base):
    __tablename__ = "user_progress"
    __table_args__ = (
        UniqueConstraint("user_id", "lesson_id", name="uq_user_progress_user_lesson"),
        Index("ix_user_progress_user_lesson", "user_id", "lesson_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("profile.id"), index=True)
    lesson_id: Mapped[int] = mapped_column(ForeignKey("lesson.id"), index=True)

    completed: Mapped[bool] = mapped_column(Boolean, default=False)
    score: Mapped[int] = mapped_column(Integer, default=0)
    xp_earned: Mapped[int] = mapped_column(Integer, default=10)

    completed_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)

    progress_user: Mapped["UserProfile"] = relationship(back_populates="user_progress")
    lesson_progress: Mapped["Lesson"] = relationship(back_populates="progress_lesson")


class XPHistory(Base):
    __tablename__ = "history"
    __table_args__ = (
        Index("ix_history_user_created", "user_id", "created_date"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("profile.id"), index=True)

    xp: Mapped[int] = mapped_column(Integer)
    reason: Mapped[str] = mapped_column(String)

    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)

    user_history: Mapped["UserProfile"] = relationship(back_populates="history_user")


class Streak(Base):
    __tablename__ = "streak"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("profile.id"), index=True)

    current_steak: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    last_activity: Mapped[date] = mapped_column(Date, default=date.today, nullable=False)

    streak_user: Mapped["UserProfile"] = relationship(back_populates="user_streak")
    rating_streak: Mapped[List["Rating"]] = relationship(
        back_populates="streak_rating",
        cascade="all, delete-orphan",
    )

    def update_after_lesson(self):
        if self.last_activity is None:
            self.last_activity = date.today()

        today = date.today()

        if self.last_activity == today:
            return self.current_steak

        if self.last_activity == today - timedelta(days=1):
            self.current_steak += 1
        else:
            self.current_steak = 1

        self.last_activity = today
        return self.current_steak


class AddFriends(Base):
    __tablename__ = "add_friends"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("profile.id"), index=True)

    add_user: Mapped["UserProfile"] = relationship(back_populates="user_add")


class Country(Base):
    __tablename__ = "country"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("profile.id"), index=True)

    user_country: Mapped["UserProfile"] = relationship(back_populates="country_user")


class Rating(Base):
    __tablename__ = "rating"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("profile.id"), index=True)
    streak_id: Mapped[int] = mapped_column(ForeignKey("streak.id"), index=True)

    user_rating: Mapped["UserProfile"] = relationship(back_populates="rating_user")
    streak_rating: Mapped["Streak"] = relationship(back_populates="rating_streak")


class LessonLevel(Base):
    __tablename__ = "lesson_level"
    __table_args__ = (
        UniqueConstraint("user_id", "lesson_id", name="uq_lesson_level_user_lesson"),
        Index("ix_lesson_level_user_lesson", "user_id", "lesson_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("profile.id"), index=True)
    lesson_id: Mapped[int] = mapped_column(ForeignKey("lesson.id"), index=True)

    level: Mapped[int] = mapped_column(Integer, default=1, server_default="1", nullable=False)
    experience: Mapped[int] = mapped_column(Integer, default=0, server_default="0", nullable=False)
    max_level: Mapped[int] = mapped_column(Integer, default=100, server_default="100", nullable=False)

    user_lesson: Mapped["UserProfile"] = relationship(back_populates="lesson_user")
    lesson: Mapped["Lesson"] = relationship(back_populates="lesson_level")

    def exp_to_next_level(self):
        if self.level is None:
            self.level = 1
        return 100 * self.level

    def add_level(self, step: int = 1):
        if self.level is None:
            self.level = 1
        if self.max_level is None:
            self.max_level = 100

        if self.level >= self.max_level:
            return self.level

        self.level = min(self.level + step, self.max_level)
        return self.level

    def add_experience(self, xp: int = 0):
        if self.level is None:
            self.level = 1
        if self.experience is None:
            self.experience = 0

        self.experience += xp

        while self.experience >= self.exp_to_next_level():
            self.experience -= self.exp_to_next_level()
            self.add_level()

        return self.level


class LessonCompletion(Base):
    __tablename__ = "lesson_completion"
    __table_args__ = (
        UniqueConstraint("user_id", "lesson_id", name="user_lesson_unique"),
        Index("ix_lesson_completion_user_lesson", "user_id", "lesson_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("profile.id"), index=True)
    lesson_id: Mapped[int] = mapped_column(ForeignKey("lesson.id"), index=True)

    date_completed: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)

    user_complete: Mapped["UserProfile"] = relationship(back_populates="complete_user")
    lesson_complete: Mapped["Lesson"] = relationship(back_populates="complete_lesson")


class Achievement(Base):
    __tablename__ = "achievement"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String, unique=True, index=True)
    code: Mapped[str] = mapped_column(String, unique=True, index=True)

    user_achievement: Mapped[List["UserAchievement"]] = relationship(
        back_populates="achievement_user",
        cascade="all, delete-orphan",
    )


class UserAchievement(Base):
    __tablename__ = "user_achievement"
    __table_args__ = (
        UniqueConstraint("user_id", "achievement_id", name="uq_user_achievement_user_achievement"),
        Index("ix_user_achievement_user_achievement", "user_id", "achievement_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("profile.id"), index=True)
    achievement_id: Mapped[int] = mapped_column(ForeignKey("achievement.id"), index=True)

    date_received: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)

    user_achievement: Mapped["UserProfile"] = relationship(back_populates="achievement_user")
    achievement_user: Mapped["Achievement"] = relationship(back_populates="user_achievement")


# =========================
# CHAT
# =========================
class ChatGroup(Base):
    __tablename__ = "group"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    owner_id: Mapped[int] = mapped_column(ForeignKey("profile.id"), index=True)
    owner: Mapped["UserProfile"] = relationship("UserProfile", back_populates="owner_group")

    title: Mapped[str] = mapped_column(String(100))
    create_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    is_private: Mapped[bool] = mapped_column(Boolean, default=False)

    group_chats: Mapped[List["GroupPeople"]] = relationship(
        back_populates="group",
        cascade="all, delete-orphan",
    )
    group_messages: Mapped[List["ChatMessage"]] = relationship(
        back_populates="group_mes",
        cascade="all, delete-orphan",
    )


class GroupPeople(Base):
    __tablename__ = "people"
    __table_args__ = (
        UniqueConstraint("group_id", "user_id", name="uq_people_group_user"),
        Index("ix_people_group_user", "group_id", "user_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    group_id: Mapped[int] = mapped_column(ForeignKey("group.id"), index=True)
    group: Mapped["ChatGroup"] = relationship("ChatGroup", back_populates="group_chats")

    user_id: Mapped[int] = mapped_column(ForeignKey("profile.id"), index=True)
    user: Mapped["UserProfile"] = relationship("UserProfile", back_populates="user_group")

    joined_date: Mapped[date] = mapped_column(Date, default=date.today)


class ChatMessage(Base):
    __tablename__ = "message"
    __table_args__ = (
        Index("ix_message_group_created", "group_id", "created_date"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    group_id: Mapped[int] = mapped_column(ForeignKey("group.id"), index=True)
    group_mes: Mapped["ChatGroup"] = relationship("ChatGroup", back_populates="group_messages")

    user_id: Mapped[int] = mapped_column(ForeignKey("profile.id"), index=True)
    user_message: Mapped["UserProfile"] = relationship("UserProfile", back_populates="user_sms")

    text: Mapped[str] = mapped_column(Text)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)

    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    edited_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)


class ChatReadState(Base):
    __tablename__ = "chat_read_state"
    __table_args__ = (
        UniqueConstraint("group_id", "user_id", name="uq_read_state_group_user"),
        Index("ix_read_state_group_user", "group_id", "user_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    group_id: Mapped[int] = mapped_column(ForeignKey("group.id"), index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("profile.id"), index=True)

    last_read_message_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
