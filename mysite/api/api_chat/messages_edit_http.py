from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from mysite.api.api_chat.deps import get_db, get_current_user
from mysite.database.models_chat import ChatMessage, GroupPeople, UserProfile
from mysite.api.api_chat.ws_messages import manager  # ✅ импорт менеджера WS (важно)

messages_edit_router = APIRouter(prefix="/messages", tags=["Messages Edit/Delete"])


class MessageEditIn(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000)


def ensure_member(db: Session, group_id: int, user_id: int) -> None:
    member = db.query(GroupPeople).filter(
        GroupPeople.group_id == group_id,
        GroupPeople.user_id == user_id
    ).first()
    if not member:
        raise HTTPException(status_code=403, detail="Not a member")


def group_member_ids(db: Session, group_id: int) -> list[int]:
    rows = db.query(GroupPeople.user_id).filter(GroupPeople.group_id == group_id).all()
    return [r[0] for r in rows]


@messages_edit_router.patch("/{message_id}")
async def edit_message(
    message_id: int,
    data: MessageEditIn,
    db: Session = Depends(get_db),
    me: UserProfile = Depends(get_current_user),
):
    msg = db.query(ChatMessage).filter(ChatMessage.id == message_id).first()
    if not msg:
        raise HTTPException(status_code=404, detail="Message not found")

    ensure_member(db, msg.group_id, me.id)

    if msg.user_id != me.id:
        raise HTTPException(status_code=403, detail="Only author can edit")

    if getattr(msg, "is_deleted", False):
        raise HTTPException(status_code=400, detail="Message already deleted")

    msg.text = data.text.strip()
    msg.edited_at = datetime.utcnow()
    db.commit()

    members = group_member_ids(db, msg.group_id)

    # ✅ WS уведомление всем
    await manager.broadcast(members, {
        "event": "message_edited",
        "message": {
            "id": msg.id,
            "group_id": msg.group_id,
            "user_id": msg.user_id,
            "text": msg.text,
            "edited_at": msg.edited_at.isoformat() if msg.edited_at else None
        }
    })

    return {"message": "edited", "id": msg.id}


@messages_edit_router.delete("/{message_id}")
async def delete_message(
    message_id: int,
    db: Session = Depends(get_db),
    me: UserProfile = Depends(get_current_user),
):
    msg = db.query(ChatMessage).filter(ChatMessage.id == message_id).first()
    if not msg:
        raise HTTPException(status_code=404, detail="Message not found")

    ensure_member(db, msg.group_id, me.id)

    if msg.user_id != me.id:
        raise HTTPException(status_code=403, detail="Only author can delete")

    # ✅ soft delete
    msg.is_deleted = True
    msg.text = ""   # можно оставить, но лучше очистить
    db.commit()

    members = group_member_ids(db, msg.group_id)

    # ✅ WS уведомление всем
    await manager.broadcast(members, {
        "event": "message_deleted",
        "message_id": msg.id,
        "group_id": msg.group_id
    })

    return {"message": "deleted", "id": msg.id}
