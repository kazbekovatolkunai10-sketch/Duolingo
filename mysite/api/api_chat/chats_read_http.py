from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime

from mysite.api.api_chat.deps import get_db, get_current_user
from mysite.database.models_chat import GroupPeople, ChatReadState, ChatMessage, UserProfile

read_router = APIRouter(prefix="/chats", tags=["Chats"])

@read_router.post("/{group_id}/read")
def mark_read(
    group_id: int,
    message_id: int = Query(..., ge=1),
    db: Session = Depends(get_db),
    me: UserProfile = Depends(get_current_user),
):
    member = db.query(GroupPeople).filter(
        GroupPeople.group_id == group_id,
        GroupPeople.user_id == me.id
    ).first()
    if not member:
        raise HTTPException(status_code=403, detail="Not a member")

    msg = db.query(ChatMessage).filter(
        ChatMessage.id == message_id,
        ChatMessage.group_id == group_id
    ).first()
    if not msg:
        raise HTTPException(status_code=404, detail="Message not found in this chat")

    state = db.query(ChatReadState).filter(
        ChatReadState.group_id == group_id,
        ChatReadState.user_id == me.id
    ).first()

    if not state:
        state = ChatReadState(
            group_id=group_id,
            user_id=me.id,
            last_read_message_id=message_id
        )
        db.add(state)
    else:
        if state.last_read_message_id is None or message_id > state.last_read_message_id:
            state.last_read_message_id = message_id
            state.updated_at = datetime.utcnow()

    db.commit()
    return {
        "message": "ok",
        "group_id": group_id,
        "last_read_message_id": message_id
    }
