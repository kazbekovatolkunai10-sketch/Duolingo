# from .db import Base
# from sqlalchemy.orm import Mapped, mapped_column, relationship
# from sqlalchemy import Integer, String, Enum, DateTime, ForeignKey, Date, Text, Boolean
# from enum import Enum as PyEnum
# from datetime import datetime, date
# from typing import List
# from sqlalchemy import UniqueConstraint
# from passlib.hash import bcrypt
# from passlib.context import CryptContext
#
#
# class StatusChoices(str, PyEnum):
#     admin = 'admin'
#     person = 'person'
#
#
# class  UserProfile(Base):
#     __tablename__ = 'profile'
#
#     id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
#     username: Mapped[str] = mapped_column(String(50))
#     email: Mapped[str] = mapped_column(String(100))
#     password: Mapped[str] = mapped_column(String)
#     user_status: Mapped[StatusChoices] = mapped_column(Enum(StatusChoices), default=StatusChoices.person)
#     date_register: Mapped[datetime] =mapped_column(DateTime, default=datetime.utcnow)
#
#     owner_group: Mapped[List["ChatGroup"]] = relationship(back_populates='owner',
#                                                          cascade='all, delete-orphan')
#     user_group: Mapped[List["GroupPeople"]] = relationship(back_populates='user',
#                                                          cascade='all, delete-orphan')
#     user_sms: Mapped[List["ChatMessage"]] = relationship(back_populates='user_message',
#                                                          cascade='all, delete-orphan')
#     refresh_tokens: Mapped[List["RefreshToken"]] = relationship(back_populates="user",
#                                                                 cascade="all, delete-orphan")
#
#     pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
#
#     def set_password(self, password: str):
#         self.password = bcrypt.hash(password)
#
#     def check_password(self, password: str):
#         return bcrypt.verify(password, self.password)
#
#     def __repr__(self):
#         return self.username
#
#
#
# class ChatGroup(Base):
#     __tablename__ = 'group'
#
#     id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
#     owner_id: Mapped[int] = mapped_column(ForeignKey('profile.id'))
#     owner: Mapped[UserProfile] = relationship(UserProfile, back_populates='owner_group')
#     title: Mapped[str] = mapped_column(String(100))
#     create_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
#     is_private: Mapped[bool] = mapped_column(default=False)
#     group_chats: Mapped[List["GroupPeople"]] = relationship(back_populates='group',
#                                                             cascade='all, delete-orphan')
#     group_messages: Mapped[List["ChatMessage"]] = relationship(back_populates='group_mes',
#                                                             cascade='all, delete-orphan')
#
# class GroupPeople(Base):
#     __tablename__ = 'people'
#
#     id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
#     group_id: Mapped[int] = mapped_column(ForeignKey('group.id'))
#     group: Mapped[ChatGroup] = relationship(ChatGroup, back_populates='group_chats')
#     user_id: Mapped[int] = mapped_column(ForeignKey('profile.id'))
#     user: Mapped[UserProfile] = relationship(UserProfile, back_populates='user_group')
#     joined_date: Mapped[date] = mapped_column(Date, default=date.today)
#
#
# class ChatMessage(Base):
#     __tablename__ = 'message'
#
#     id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
#     group_id: Mapped[int] = mapped_column(ForeignKey('group.id'))
#     group_mes: Mapped[ChatGroup] = relationship(ChatGroup, back_populates='group_messages')
#     user_id: Mapped[int] = mapped_column(ForeignKey('profile.id'))
#     user_message: Mapped[UserProfile] = relationship(UserProfile, back_populates='user_sms')
#     text: Mapped[str] = mapped_column(Text)
#     created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
#     is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
#     edited_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
#
#
# class RefreshToken(Base):
#     __tablename__ = "refresh_token"
#
#     id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
#     token: Mapped[str] = mapped_column(String, unique=True, nullable=False)
#     created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
#     user_id: Mapped[int] = mapped_column(ForeignKey('profile.id'),nullable=False)
#
#     user: Mapped[UserProfile] = relationship(UserProfile, back_populates="refresh_tokens")
#
#
# class ChatReadState(Base):
#     __tablename__ = "chat_read_state"
#
#     id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
#
#     group_id: Mapped[int] = mapped_column(ForeignKey("group.id"), index=True)
#     user_id: Mapped[int] = mapped_column(ForeignKey("profile.id"), index=True)
#
#     last_read_message_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
#     updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
#
#     __table_args__ = (
#         UniqueConstraint("group_id", "user_id", name="uq_read_state_group_user"),
#     )
#