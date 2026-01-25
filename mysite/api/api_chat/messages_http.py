from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from mysite.api.api_chat.deps import get_db, get_current_user
from mysite.database.models import ChatMessage, GroupPeople, UserProfile
from mysite.database.schema import MessagesPageOut, MessageOut

messages_http = APIRouter(prefix="/groups", tags=["Messages (HTTP)"])


@messages_http.get("/{group_id}/messages", response_model=MessagesPageOut)
def fetch_messages(
    group_id: int,
    limit: int = Query(default=50, ge=1, le=200),
    before_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
    me: UserProfile = Depends(get_current_user),
):
    is_member = db.query(GroupPeople).filter(
        GroupPeople.group_id == group_id,
        GroupPeople.user_id == me.id
    ).first()
    if not is_member:
        raise HTTPException(status_code=403, detail="Not a member")

    q = db.query(ChatMessage).filter(ChatMessage.group_id == group_id)
    if before_id is not None:
        q = q.filter(ChatMessage.id < before_id)

    rows = q.order_by(ChatMessage.id.desc()).limit(limit + 1).all()
    has_more = len(rows) > limit
    rows = rows[:limit]
    rows = list(reversed(rows))

    next_before = rows[0].id if rows else before_id

    return {
        "group_id": group_id,
        "items": rows,
        "has_more": has_more,
        "before_id": next_before
    }
