from fastapi import APIRouter, Depends, HTTPException, status
from ..schema.milestone_schema import MilestoneCreate, MilestoneUpdate, MilestoneResponse
from sqlalchemy.orm import Session
from ..DataBase.db_dependency import get_db
from ..DataBase import db_model
from ..utils.auth_utils import get_current_user
from typing import Annotated


router = APIRouter(
    tags=["milestones"],
    prefix="/milestones"
)

@router.get("/test")
async def root():
    return {"message": "this is milestones"}


# create milestone by admin
@router.post("/milestones/", response_model=MilestoneResponse, status_code=status.HTTP_201_CREATED)
def create_milestone(current_user: Annotated[db_model.User, Depends(get_current_user)], milestone: MilestoneCreate, db: Session = Depends(get_db)):
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can create milestones")
    new_milestone = db_model.Milestone(
        name=milestone.name,
        description=milestone.description
    )
    db.add(new_milestone)
    db.commit()
    db.refresh(new_milestone)
    return new_milestone


# get all milestones for user and admin
@router.get("/all/", response_model=list[MilestoneResponse], status_code=status.HTTP_200_OK)
def get_all_milestones(db: Session = Depends(get_db)):
    milestones = db.query(db_model.Milestone).all()
    return milestones

# get milestone by id for user and admin
@router.get("/{milestone_id}", response_model=MilestoneResponse, status_code=status.HTTP_200_OK)
def get_milestone_by_id(milestone_id: int, db: Session = Depends(get_db)):
    milestone = db.query(db_model.Milestone).filter(db_model.Milestone.id == milestone_id).first()
    if not milestone:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Milestone not found")
    return milestone


# update milestone by admin
@router.put("/{milestone_id}", response_model=MilestoneResponse,status_code=status.HTTP_200_OK)
def update_milestone(current_user: Annotated[db_model.User, Depends(get_current_user)], milestone_id: int, milestone: MilestoneUpdate, db: Session = Depends(get_db)):
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can update milestones")
    existing_milestone = db.query(db_model.Milestone).filter(db_model.Milestone.id == milestone_id).first()
    if not existing_milestone:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Milestone not found")
    existing_milestone.name = milestone.name
    existing_milestone.description = milestone.description
    db.commit()
    db.refresh(existing_milestone)
    return existing_milestone

# delete milestone by admin
@router.delete("/{milestone_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_milestone(current_user: Annotated[db_model.User, Depends(get_current_user)], milestone_id: int, db: Session = Depends(get_db)):
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can delete milestones")
    milestone = db.query(db_model.Milestone).filter(db_model.Milestone.id == milestone_id).first()
    if not milestone:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Milestone not found")
    db.delete(milestone)
    db.commit()
    return {"message": "Milestone deleted successfully"}

