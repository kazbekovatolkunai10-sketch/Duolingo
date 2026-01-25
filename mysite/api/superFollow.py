from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from mysite.database.models import SuperFollow
from mysite.database.schema import SuperFollowOutSchema, SuperFollowInputSchema
from mysite.database.db import SessionLocal

super_follow_router = APIRouter(prefix="/super_follow", tags=["Super Follow"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ✅ CREATE
@super_follow_router.post("/", response_model=SuperFollowOutSchema, status_code=201)
def create_super_follow(
    payload: SuperFollowInputSchema,
    db: Session = Depends(get_db),
):
    obj = SuperFollow(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


# ✅ LIST
@super_follow_router.get("/", response_model=List[SuperFollowOutSchema])
def list_super_follow(db: Session = Depends(get_db)):
    return db.query(SuperFollow).order_by(SuperFollow.id.desc()).all()


# ✅ DETAIL
@super_follow_router.get("/{super_follow_id}", response_model=SuperFollowOutSchema)
def detail_super_follow(
    super_follow_id: int,
    db: Session = Depends(get_db),
):
    obj = db.query(SuperFollow).filter(SuperFollow.id == super_follow_id).first()
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="SuperFollow not found",
        )
    return obj


# ✅ UPDATE (partial)
@super_follow_router.patch("/{super_follow_id}", response_model=SuperFollowOutSchema)
def update_super_follow(
    super_follow_id: int,
    payload: SuperFollowInputSchema,
    db: Session = Depends(get_db),
):
    obj = db.query(SuperFollow).filter(SuperFollow.id == super_follow_id).first()
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="SuperFollow not found",
        )

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(obj, key, value)

    db.commit()
    db.refresh(obj)
    return obj


# ✅ DELETE
@super_follow_router.delete("/{super_follow_id}", response_model=dict)
def delete_super_follow(
    super_follow_id: int,
    db: Session = Depends(get_db),
):
    obj = db.query(SuperFollow).filter(SuperFollow.id == super_follow_id).first()
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="SuperFollow not found",
        )

    db.delete(obj)
    db.commit()
    return {"message": "deleted"}
