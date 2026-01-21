from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime


class UserCreateSchema(BaseModel):
    email: EmailStr
    username: str
    password: str


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str


class UserResponseSchema(BaseModel):
    id: int
    email: EmailStr
    username: str
    date_register: datetime

    class Config:
        from_attributes = True



class GroupCreateIn(BaseModel):
    title: str


class GroupOut(BaseModel):
    id: int
    owner_id: int
    title: str
    create_date: datetime

    class Config:
        from_attributes = True


class AddMembersIn(BaseModel):
    user_ids: List[int]


class MessageOut(BaseModel):
    id: int
    group_id: int
    user_id: int
    text: str
    created_date: datetime

    class Config:
        from_attributes = True


class MessagesPageOut(BaseModel):
    group_id: int
    items: List[MessageOut]
    has_more: bool
    before_id: Optional[int] = None



# chat_list
class LastMessageOut(BaseModel):
    id: int
    user_id: int
    text: str
    created_date: datetime

    class Config:
        from_attributes = True


class ChatListItemOut(BaseModel):
    group_id: int
    title: Optional[str] = None
    is_private: bool
    members_count: int
    last_message: Optional[LastMessageOut] = None
    unread_count: int
