from .db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, DateTime, Date, Boolean, Text, Enum
from datetime import date, datetime
from typing import List, Optional
from enum import Enum as PyEnum


class RoleChoices(str, PyEnum):
    user = 'user'
    admin = 'admin'

class LevelChoices(str, PyEnum):
    A1 = 'A1'
    A2 = 'A2'
    B1 = 'B1'
    B2 = 'B2'
    C1 = 'C1'
    C2 = 'C2'

class TypeChoices(str, PyEnum):
    private = 'private'
    group = 'group'

class UserProfile(Base):
    __tablename__ = 'profile'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    avatar: Mapped[Optional[str]] = mapped_column(String)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(60))
    username: Mapped[str] = mapped_column(String, unique=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String)
    phone_number: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    role: Mapped[RoleChoices] = mapped_column(Enum(RoleChoices), default=RoleChoices.user)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)
    date_register: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


    following_user: Mapped[List['Follow']] = relationship(back_populates='following',
                                                          cascade='all, delete-orphan', foreign_keys='Follow.following_id')
    follower_user: Mapped[List['Follow']] = relationship(back_populates='follower',
                                                         cascade='all, delete-orphan', foreign_keys='Follow.follower_id')
    user_progress: Mapped[List['UserProgres']] = relationship(back_populates='progress_user',
                                                              cascade='all, delete-orphan')
    history_user: Mapped[List['XPHistory']] = relationship(back_populates='user_history',
                                                           cascade='all, delete-orphan')
    user_streak: Mapped[List['Streak']] = relationship(back_populates='streak_user',
                                                       cascade='all, delete-orphan')
    member_user: Mapped[List['ChatMember']] = relationship(back_populates='user_member',
                                                           cascade='all, delete-orphan')
    user_add: Mapped[List['AddFriends']] = relationship(back_populates='add_user',
                                                        cascade='all, delete-orphan')
    country_user: Mapped[List['Country']] = relationship(back_populates='user_country',
                                                          cascade='all, delete-orphan')
    rating_user: Mapped[List['Rating']] = relationship(back_populates='user_rating',
                                                       cascade='all, delete-orphan')
    user_lesson_level: Mapped[List['LessonLevel']] = relationship(back_populates='lesson_level_user',
                                                                  cascade='all, delete-orphan')
    user_token: Mapped[List['RefreshToken']] = relationship(back_populates='token_user',
                                                            cascade='all, delete-orphan')

    def __repr__(self):
        return f'{self.first_name}, {self.last_name}'


class RefreshToken(Base):
    __tablename__ = 'refresh_token'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('profile.id'))
    token: Mapped[str] = mapped_column(String)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow())

    token_user: Mapped[UserProfile] = relationship(back_populates='user_token')


class Follow(Base):
    __tablename__ = 'follow'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    following_id: Mapped[int] = mapped_column(ForeignKey('profile.id'))
    follower_id: Mapped[int] = mapped_column(ForeignKey('profile.id'))


    following: Mapped[UserProfile] = relationship(back_populates='following_user', foreign_keys=[following_id])
    follower: Mapped[UserProfile] = relationship(back_populates='follower_user', foreign_keys=[follower_id])


class SuperFollow(Base):
    __tablename__ = 'super_follow'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(Text)


class FamilyFollow(Base):
    __tablename__ = 'family_follow'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(Text)


class MaxFollow(Base):
    __tablename__ = 'max_follow'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(Text)


class Language(Base):
    __tablename__ = 'language'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String, unique=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    is_active: Mapped[bool] = mapped_column(Boolean)


    course_language: Mapped[List['Course']] = relationship(back_populates='language',
                                                           cascade='all, delete-orphan')
    chat_language: Mapped[List['Chat']] = relationship(back_populates='language_chat',
                                                       cascade='all, delete-orphan')

class Course(Base):
    __tablename__ = 'course'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    language_id: Mapped[int] = mapped_column(ForeignKey('language.id'))
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(Text)
    level: Mapped[LevelChoices] = mapped_column(Enum(LevelChoices), default=LevelChoices.A1)
    order: Mapped[int] = mapped_column(Integer)


    language: Mapped[Language] = relationship(back_populates='course_language')
    lesson_course: Mapped[List['Lesson']] = relationship(back_populates='course_lesson',
                                                         cascade='all, delete-orphan')

class Lesson(Base):
    __tablename__ = 'lesson'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    course_id: Mapped[int] = mapped_column(ForeignKey('course.id'))
    title: Mapped[str] = mapped_column(String)
    order: Mapped[int] = mapped_column(Integer)
    is_locked: Mapped[bool] = mapped_column(Boolean, default=False)


    course_lesson: Mapped[Course] = relationship(back_populates='lesson_course')
    exercise_lesson: Mapped[List['Exercise']] = relationship(back_populates='lesson',
                                                             cascade='all, delete-orphan')
    progress_lesson: Mapped[List['UserProgres']] = relationship(back_populates='lesson_progress',
                                                                cascade='all, delete')

class Exercise(Base):
    __tablename__ = 'exercise'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    lesson_id: Mapped[int] = mapped_column(ForeignKey('lesson.id'))
    type: Mapped[LevelChoices] = mapped_column(Enum(LevelChoices))
    questions: Mapped[str] = mapped_column(Text)
    correct_answer: Mapped[str] = mapped_column(String)


    lesson: Mapped[Lesson] = relationship(back_populates='exercise_lesson')
    option: Mapped[List['Option']] = relationship(back_populates='exercise',
                                                  cascade='all, delete-orphan')

class Option(Base):
    __tablename__ = 'option'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    exercise_id: Mapped[int] = mapped_column(ForeignKey('exercise.id'))


    exercise: Mapped[Exercise] = relationship(back_populates='option')


class UserProgres(Base):
    __tablename__ = 'user_progress'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('profile.id'))
    lesson_id: Mapped[int] = mapped_column(ForeignKey('lesson.id'))
    completed: Mapped[bool] = mapped_column(Boolean, default=False)
    score: Mapped[int] = mapped_column(Integer)
    completed_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


    progress_user: Mapped[UserProfile] = relationship(back_populates='user_progress')
    lesson_progress: Mapped[Lesson] = relationship(back_populates='progress_lesson')


class XPHistory(Base):
    __tablename__ = 'history'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('profile.id'))
    xp: Mapped[int] = mapped_column(Integer)
    reason: Mapped[str] = mapped_column(String)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


    user_history: Mapped[UserProfile] = relationship(back_populates='history_user')

class Streak(Base):
    __tablename__ = 'streak'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('profile.id'))
    current_steak: Mapped[int] = mapped_column(Integer)
    last_activity: Mapped[date] = mapped_column(Date, default=date.today)


    streak_user: Mapped[UserProfile] = relationship(back_populates='user_streak')
    rating_streak: Mapped[List['Rating']] = relationship(back_populates='streak_rating',
                                                         cascade='all, delete-orphan')


class Chat(Base):
    __tablename__ = 'chat'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    type: Mapped[TypeChoices] = mapped_column(Enum(TypeChoices))
    language_id: Mapped[int] = mapped_column(ForeignKey('language.id'))
    create_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


    language_chat: Mapped[Language] = relationship(back_populates='chat_language')
    member_chat: Mapped[List['ChatMember']] = relationship(back_populates='chat_member',
                                                           cascade='all, delete-orphan')
    message_chat: Mapped[List['Message']] = relationship(back_populates='chat_message',
                                                         cascade='all, delete-orphan')

class ChatMember(Base):
    __tablename__ = 'chat_member'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    chat_id: Mapped[int] = mapped_column(ForeignKey('chat.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('profile.id'))
    joined_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


    chat_member: Mapped[Chat] = relationship(back_populates='member_chat')
    user_member: Mapped[UserProfile] = relationship(back_populates='member_user')
    message_sender: Mapped[List['Message']] = relationship(back_populates='sender_message',
                                                           cascade='all, delete-orphan')

class Message(Base):
    __tablename__ = 'message'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    chat_id: Mapped[int] = mapped_column(ForeignKey('chat.id'))
    sender_id: Mapped[int] = mapped_column(ForeignKey('chat_member.id'))
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)


    chat_message: Mapped[Chat] = relationship(back_populates='message_chat')
    sender_message: Mapped[ChatMember] = relationship(back_populates='message_sender')


class AddFriends(Base):
    __tablename__ = 'add_friends'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('profile.id'))

    add_user: Mapped[UserProfile] = relationship(back_populates='user_add')


class Country(Base):
    __tablename__ = 'country'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('profile.id'))

    user_country: Mapped[UserProfile] = relationship(back_populates='country_user')


class Rating(Base):
    __tablename__ = 'rating'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('profile.id'))
    streak_id: Mapped[int] = mapped_column(ForeignKey('streak.id'))

    user_rating: Mapped[UserProfile] = relationship(back_populates='rating_user')
    streak_rating: Mapped[Streak] = relationship(back_populates='rating_streak')


class LessonLevel(Base):
    __tablename__ = 'lesson_level'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('profile.id'))
    level: Mapped[int] = mapped_column(Integer, default=1)

    lesson_level_user: Mapped[UserProfile] = relationship(back_populates='user_lesson_level')
    level_lesson: Mapped[List['Achievement']] = relationship(back_populates='lesson_level',
                                                             cascade='all, delete-orphan')

    @property
    def add_level(self):
        if self.level < 101:
            self.level += 1
        return self.level


class Achievement(Base):
    __tablename__ = 'achievement'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    lesson_level_id: Mapped[int] = mapped_column(ForeignKey('lesson_level.id'))

    lesson_level: Mapped[LessonLevel] = relationship(back_populates='level_lesson')
