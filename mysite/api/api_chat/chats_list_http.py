from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, select

from mysite.api.api_chat.deps import get_db, get_current_user
from mysite.database.models import ChatGroup, GroupPeople, ChatMessage, ChatReadState, UserProfile
from mysite.database.schema import ChatListItemOut, LastMessageOut

chats_router = APIRouter(prefix="/chats", tags=["Chats"])


@chats_router.get("/my", response_model=list[ChatListItemOut])
def my_chats(
    db: Session = Depends(get_db),
    me: UserProfile = Depends(get_current_user),
):
    my_group_ids_sel = select(GroupPeople.group_id).where(GroupPeople.user_id == me.id)

    members_count_sq = (
        db.query(
            GroupPeople.group_id.label("gid"),
            func.count(GroupPeople.id).label("members_count"),
        )
        .filter(GroupPeople.group_id.in_(my_group_ids_sel))
        .group_by(GroupPeople.group_id)
        .subquery()
    )

    last_msg_sq = (
        db.query(
            ChatMessage.group_id.label("gid"),
            func.max(ChatMessage.id).label("last_message_id"),
        )
        .filter(ChatMessage.group_id.in_(my_group_ids_sel))
        .group_by(ChatMessage.group_id)
        .subquery()
    )

    rows = (
        db.query(ChatGroup, members_count_sq.c.members_count, last_msg_sq.c.last_message_id)
        .join(members_count_sq, members_count_sq.c.gid == ChatGroup.id)
        .outerjoin(last_msg_sq, last_msg_sq.c.gid == ChatGroup.id)
        .filter(ChatGroup.id.in_(my_group_ids_sel))
        .order_by(ChatGroup.create_date.desc())
        .all()
    )

    # last messages batch
    last_ids = [r[2] for r in rows if r[2] is not None]
    last_map = {}
    if last_ids:
        msgs = db.query(ChatMessage).filter(ChatMessage.id.in_(last_ids)).all()
        last_map = {m.id: m for m in msgs}

    # read states batch
    group_ids = [r[0].id for r in rows]
    states_map = {}
    if group_ids:
        states = (
            db.query(ChatReadState)
            .filter(ChatReadState.user_id == me.id, ChatReadState.group_id.in_(group_ids))
            .all()
        )
        states_map = {s.group_id: s for s in states}

    items: list[ChatListItemOut] = []

    for g, members_count, last_message_id in rows:
        last_msg_out = None
        if last_message_id is not None and last_message_id in last_map:
            m = last_map[last_message_id]
            last_msg_out = LastMessageOut(
                id=m.id,
                user_id=m.user_id,
                text="" if m.is_deleted else m.text,
                created_date=m.created_date,
            )

        state = states_map.get(g.id)
        last_read_id = state.last_read_message_id if state else None

        unread_q = db.query(func.count(ChatMessage.id)).filter(ChatMessage.group_id == g.id)
        if last_read_id is not None:
            unread_q = unread_q.filter(ChatMessage.id > last_read_id)
        unread_count = int(unread_q.scalar() or 0)

        items.append(
            ChatListItemOut(
                group_id=g.id,
                title=g.title,
                is_private=bool(g.is_private),          # ✅ берём из поля модели
                members_count=int(members_count or 0),
                last_message=last_msg_out,
                unread_count=unread_count,
            )
        )

    return items
