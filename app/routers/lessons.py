from fastapi import APIRouter, Depends, HTTPException, status
from ..schema.user_schema import LearningResourceCreate, LearningResourceUpdate, LearningResourceResponse
from sqlalchemy.orm import Session
from ..DataBase.db_dependency import get_db
from ..DataBase import db_model
from ..utils.auth_utils import get_current_user
from typing import Annotated





router = APIRouter(
    tags=["lessons"],
    prefix="/lessons"
)

# testing route
@router.get("/test")
async def root():
    return {"message": "Hello World"}

# get all resources
@router.get("/get-all-learning-resources/", response_model=list[LearningResourceResponse])
def get_all_learning_resources(db: Session = Depends(get_db)):
    resources = db.query(db_model.Lesson).all()
    return resources

# for admin to create resources
@router.post("/learning-resources/", response_model=LearningResourceResponse, status_code=status.HTTP_201_CREATED)
def create_learning_resource(current_user: Annotated[db_model.User, Depends(get_current_user)],resource: LearningResourceCreate, db: Session = Depends(get_db)):
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can create resources")
    new_resource = db_model.Lesson(
        title=resource.title,
        description=resource.description,
        video_url=resource.video_url
    )
    db.add(new_resource)
    db.commit()
    db.refresh(new_resource)
    return new_resource

# for admin to update resources
@router.put("/learning-resources/{resource_id}", response_model=LearningResourceResponse)
def update_learning_resource(current_user: Annotated[db_model.User, Depends(get_current_user)],resource_id: int, resource: LearningResourceUpdate, db: Session = Depends(get_db)):
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can create resources")
    existing_resource = db.query(db_model.Lesson).filter(db_model.Lesson.id == resource_id).first()
    if not existing_resource:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")
    existing_resource.title = resource.title
    existing_resource.description = resource.description
    existing_resource.video_url = resource.video_url
    db.commit()
    db.refresh(existing_resource)
    return existing_resource


# for admin to delete resources
@router.delete("/learning-resources/{resource_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_learning_resource(current_user: Annotated[db_model.User, Depends(get_current_user)],resource_id: int, db: Session = Depends(get_db)):
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can create resources")
    resource = db.query(db_model.Lesson).filter(db_model.Lesson.id == resource_id).first()
    if not resource:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")
    db.delete(resource if resource else None)
    db.commit()
    return {"message": "Resource deleted"}



# for both admin and user to get resources
@router.get("/learning-resources/{resource_id}", response_model=LearningResourceResponse)
def get_learning_resource(current_user: Annotated[db_model.User, Depends(get_current_user)],resource_id: int, db: Session = Depends(get_db)):
    if current_user.role != "admin" or current_user.role != "user":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can create resources")
    resource = db.query(db_model.Lesson).filter(db_model.Lesson.id == resource_id).first()
    if not resource:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")
    return resource




