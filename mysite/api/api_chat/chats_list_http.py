from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from mysite.api.api_chat.deps import get_db, get_current_user
from mysite.database.models_chat import ChatGroup, GroupPeople, ChatMessage, ChatReadState, UserProfile
from mysite.database.schema_chat import ChatListItemOut

chats_router = APIRouter(prefix="/chats", tags=["Chats"])


@chats_router.get("/my", response_model=list[ChatListItemOut])
def my_chats(
    db: Session = Depends(get_db),
    me: UserProfile = Depends(get_current_user),
):
    # мои группы (в которых я участник)
    my_group_ids = (
        db.query(GroupPeople.group_id)
        .filter(GroupPeople.user_id == me.id)
        .subquery()
    )

    # members_count по каждой группе
    members_count_sq = (
        db.query(
            GroupPeople.group_id.label("gid"),
            func.count(GroupPeople.id).label("members_count")
        )
        .filter(GroupPeople.group_id.in_(my_group_ids))
        .group_by(GroupPeople.group_id)
        .subquery()
    )

    # last_message_id по каждой группе
    last_msg_sq = (
        db.query(
            ChatMessage.group_id.label("gid"),
            func.max(ChatMessage.id).label("last_message_id")
        )
        .filter(ChatMessage.group_id.in_(my_group_ids))
        .group_by(ChatMessage.group_id)
        .subquery()
    )

    # основной список
    rows = (
        db.query(ChatGroup, members_count_sq.c.members_count, last_msg_sq.c.last_message_id)
        .join(members_count_sq, members_count_sq.c.gid == ChatGroup.id)
        .outerjoin(last_msg_sq, last_msg_sq.c.gid == ChatGroup.id)
        .filter(ChatGroup.id.in_(my_group_ids))
        .order_by(ChatGroup.id.desc())
        .all()
    )

    items: list[ChatListItemOut] = []

    for g, members_count, last_message_id in rows:
        # last_message
        last_msg = None
        if last_message_id:
            last_msg = db.query(ChatMessage).filter(ChatMessage.id == last_message_id).first()

        # last_read_message_id
        state = db.query(ChatReadState).filter(
            ChatReadState.group_id == g.id,
            ChatReadState.user_id == me.id
        ).first()
        last_read_id = state.last_read_message_id if state else None

        # unread_count
        unread_q = db.query(func.count(ChatMessage.id)).filter(ChatMessage.group_id == g.id)
        if last_read_id is not None:
            unread_q = unread_q.filter(ChatMessage.id > last_read_id)
        unread_count = unread_q.scalar() or 0

        items.append(ChatListItemOut(
            group_id=g.id,
            title=g.title,
            is_private=(members_count == 2),
            members_count=members_count,
            last_message=last_msg,
            unread_count=unread_count,
        ))

    return items
