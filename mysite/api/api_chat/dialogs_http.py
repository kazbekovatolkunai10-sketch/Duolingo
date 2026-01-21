from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from mysite.api.api_chat.deps import get_db, get_current_user
from mysite.database.models_chat import ChatGroup, GroupPeople, UserProfile

dialogs_router = APIRouter(prefix="/dialogs", tags=["Dialogs"])


def make_dialog_title(me_id: int, other_id: int) -> str:
    a, b = (me_id, other_id) if me_id < other_id else (other_id, me_id)
    return f"dialog_{a}_{b}"


@dialogs_router.post("/{other_user_id}")
def get_or_create_dialog(
    other_user_id: int,
    db: Session = Depends(get_db),
    me: UserProfile = Depends(get_current_user),
):
    if other_user_id == me.id:
        raise HTTPException(status_code=400, detail="Cannot chat with yourself")

    other = db.query(UserProfile).filter(UserProfile.id == other_user_id).first()
    if not other:
        raise HTTPException(status_code=404, detail="User not found")

    # ✅ Ищем существующий диалог:
    # группы где есть me и other и участников ровно 2
    my_group_ids = (
        db.query(GroupPeople.group_id)
        .filter(GroupPeople.user_id == me.id)
        .subquery()
    )

    other_group_ids = (
        db.query(GroupPeople.group_id)
        .filter(GroupPeople.user_id == other_user_id)
        .subquery()
    )

    candidate_ids = (
        db.query(GroupPeople.group_id)
        .filter(GroupPeople.group_id.in_(my_group_ids))
        .filter(GroupPeople.group_id.in_(other_group_ids))
        .subquery()
    )

    row = (
        db.query(GroupPeople.group_id)
        .filter(GroupPeople.group_id.in_(candidate_ids))
        .group_by(GroupPeople.group_id)
        .having(func.count(GroupPeople.user_id) == 2)
        .first()
    )

    if row:
        return {"dialog_id": row[0], "created": False}

    # ✅ Создаём новый диалог (title НЕ None!)
    dialog = ChatGroup(
        title=make_dialog_title(me.id, other_user_id),
        owner_id=me.id
    )
    db.add(dialog)
    db.commit()
    db.refresh(dialog)

    db.add_all([
        GroupPeople(group_id=dialog.id, user_id=me.id),
        GroupPeople(group_id=dialog.id, user_id=other_user_id),
    ])
    db.commit()

    return {"dialog_id": dialog.id, "created": True}
