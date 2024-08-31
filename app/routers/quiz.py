from fastapi import APIRouter, Depends, HTTPException, status
from ..schema.quiz_schema import QuizCreate, QuizUpdate, QuizResponse
from sqlalchemy.orm import Session
from ..DataBase.db_dependency import get_db
from ..DataBase import db_model
from ..utils.auth_utils import get_current_user
from typing import Annotated

router = APIRouter(
    tags=["quiz"],
    prefix="/quiz"
)
@router.get("/test")
async def root():
    return {"message": "quiz routes"}

