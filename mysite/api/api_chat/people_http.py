from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from mysite.api.api_chat.deps import get_db, get_current_user
from mysite.database.models_chat import ChatGroup, GroupPeople, UserProfile
from mysite.database.schema_chat import AddMembersIn

people_http = APIRouter(prefix="/groups", tags=["Group Members"])


def _require_owner(db: Session, group_id: int, me_id: int) -> ChatGroup:
    g = db.query(ChatGroup).filter(ChatGroup.id == group_id).first()
    if not g:
        raise HTTPException(status_code=404, detail="Group not found")
    if g.owner_id != me_id:
        raise HTTPException(status_code=403, detail="Only owner can manage members")
    return g


@people_http.post("/{group_id}/members")
def add_members(
    group_id: int,
    data: AddMembersIn,
    db: Session = Depends(get_db),
    me: UserProfile = Depends(get_current_user),
):
    _require_owner(db, group_id, me.id)

    added = []
    for uid in data.user_ids:
        if not isinstance(uid, int) or uid <= 0:
            continue

        exists_user = db.query(UserProfile.id).filter(UserProfile.id == uid).first()
        if not exists_user:
            continue

        already = db.query(GroupPeople.id).filter(
            GroupPeople.group_id == group_id,
            GroupPeople.user_id == uid
        ).first()
        if already:
            continue

        db.add(GroupPeople(group_id=group_id, user_id=uid))
        added.append(uid)

    db.commit()
    return {"group_id": group_id, "added_user_ids": added}


@people_http.delete("/{group_id}/members/{user_id}")
def remove_member(
    group_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    me: UserProfile = Depends(get_current_user),
):
    g = db.query(ChatGroup).filter(ChatGroup.id == group_id).first()
    if not g:
        raise HTTPException(status_code=404, detail="Group not found")

    # удалять может owner или сам user_id
    if me.id != g.owner_id and me.id != user_id:
        raise HTTPException(status_code=403, detail="No permission")

    if user_id == g.owner_id:
        raise HTTPException(status_code=400, detail="Owner cannot be removed")

    row = db.query(GroupPeople).filter(
        GroupPeople.group_id == group_id,
        GroupPeople.user_id == user_id
    ).first()
    if not row:
        raise HTTPException(status_code=404, detail="User not in group")

    db.delete(row)
    db.commit()
    return {"message": "removed"}
