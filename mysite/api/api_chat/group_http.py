from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from mysite.api.api_chat.deps import get_db, get_current_user
from mysite.database.models_chat import ChatGroup, GroupPeople, UserProfile
from mysite.database.schema_chat import GroupCreateIn, GroupOut

group_http = APIRouter(prefix="/groups", tags=["Groups"])


@group_http.post("", response_model=GroupOut)
def create_group(
    data: GroupCreateIn,
    db: Session = Depends(get_db),
    me: UserProfile = Depends(get_current_user),
):
    title = (data.title or "").strip()
    if not title:
        raise HTTPException(status_code=400, detail="title is required")

    g = ChatGroup(title=title, owner_id=me.id)
    db.add(g)
    db.commit()
    db.refresh(g)

    # создателя сразу в участники
    db.add(GroupPeople(group_id=g.id, user_id=me.id))
    db.commit()

    return g


@group_http.get("", response_model=list[GroupOut])
def my_groups(
    db: Session = Depends(get_db),
    me: UserProfile = Depends(get_current_user),
):
    groups = (
        db.query(ChatGroup)
        .join(GroupPeople, GroupPeople.group_id == ChatGroup.id)
        .filter(GroupPeople.user_id == me.id)
        .order_by(ChatGroup.id.desc())
        .all()
    )
    return groups


@group_http.get("/{group_id}", response_model=GroupOut)
def group_detail(
    group_id: int,
    db: Session = Depends(get_db),
    me: UserProfile = Depends(get_current_user),
):
    g = db.query(ChatGroup).filter(ChatGroup.id == group_id).first()
    if not g:
        raise HTTPException(status_code=404, detail="Group not found")

    is_member = db.query(GroupPeople).filter(
        GroupPeople.group_id == group_id,
        GroupPeople.user_id == me.id
    ).first()
    if not is_member:
        raise HTTPException(status_code=403, detail="Not a member")

    return g
