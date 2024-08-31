# main.py
from fastapi import FastAPI
from .routers import auth, lessons,milestone,Badges
# milestones, users_info, quizzes

app = FastAPI()

app.include_router(auth.router)
app.include_router(lessons.router)
app.include_router(milestone.router)
app.include_router(Badges.router)