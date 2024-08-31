from fastapi import APIRouter, Depends, HTTPException, status
from ..schema.badge_schema import BadgeCreate, BadgeUpdate, BadgeResponse
from sqlalchemy.orm import Session
from ..DataBase.db_dependency import get_db
from ..DataBase import db_model
from ..utils.auth_utils import get_current_user
from typing import Annotated


router = APIRouter(
    tags=["badges"],
    prefix="/badges"
)

# testing route
@router.get("/test")
async def root():
    return {"message": "this is badges"}

# create badge by admin
@router.post("/badges/", response_model=BadgeResponse, status_code=status.HTTP_201_CREATED)
async def create_badge(current_user: Annotated[db_model.User, Depends(get_current_user)], badge: BadgeCreate, db: Session = Depends(get_db)):
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can create badges")
    new_badge = db_model.Badge(
        name=badge.name,
        description=badge.description,
        image_url=badge.image_url
    )
    db.add(new_badge)
    db.commit()
    db.refresh(new_badge)
    return new_badge


# get all the badges for user and admin
@router.get("/all/", response_model=list[BadgeResponse], status_code=status.HTTP_200_OK)
def get_all_badges(db: Session = Depends(get_db)):
    badges = db.query(db_model.Badge).all()
    return badges

# update badge by admin
@router.put("/{badge_id}", response_model=BadgeResponse, status_code=status.HTTP_200_OK)
def update_badge(current_user: Annotated[db_model.User, Depends(get_current_user)], badge_id: int, badge: BadgeUpdate, db: Session = Depends(get_db)):
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can update badges")
    existing_badge = db.query(db_model.Badge).filter(db_model.Badge.id == badge_id).first()
    if not existing_badge:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Badge not found")
    existing_badge.name = badge.name
    existing_badge.description = badge.description
    db.commit()
    db.refresh(existing_badge)


# get badge by id for user and admin
@router.get("/{badge_id}", response_model=BadgeResponse, status_code=status.HTTP_200_OK)
def get_badge_by_id(badge_id: int, db: Session = Depends(get_db)):
    badge = db.query(db_model.Badge).filter(db_model.Badge.id == badge_id).first()
    if not badge:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Badge not found")
    return badge

# delete badge by admin
@router.delete("/{badge_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_badge(current_user: Annotated[db_model.User, Depends(get_current_user)], badge_id: int, db: Session = Depends(get_db)):
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can delete badges")
    badge = db.query(
        db_model.Badge).filter(db_model.Badge.id == badge_id).first()
    if not badge:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Badge not found")
    db.delete(badge)
    db.commit()
    return {"message": "Badge deleted successfully"}


