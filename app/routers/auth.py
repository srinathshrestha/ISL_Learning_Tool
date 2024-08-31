# routers/auth.py

from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from ..DataBase.db_dependency import get_db
from ..DataBase import db_model
from ..schema.user_schema import UserCreate, UserResponse, UserLogin, TokenRespose
from ..utils.auth_utils import authenticate_user, create_access_token, get_current_user,bcrypt_context,oauth2_bearer  # Import utility functions

router = APIRouter(
    tags=["auth"],
    prefix="/auth"
)


@router.post("/users/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(db_model.User).filter(
        (db_model.User.username == user.username) | 
        (db_model.User.email == user.email)
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered"
        )
    
    hashed_password = bcrypt_context.hash(user.password)
    db_user = db_model.User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password, 
        role=user.role
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

@router.post("/login/", status_code=status.HTTP_202_ACCEPTED, response_model=TokenRespose)
def login_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    token = create_access_token(
        user.username,
        user.id,
        user.role,
        timedelta(minutes=20)
    )
    return {
        "access_token": token,
        "token_type": "bearer"
    }

# Ensure to include this if you have routes that require authentication
@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: Annotated[db_model.User, Depends(get_current_user)]):
    return current_user
