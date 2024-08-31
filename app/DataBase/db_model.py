from datetime import datetime, timezone
from .db_conn import Base
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String, default='user')
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc))

    # Relationships with other models
    progress = relationship('UserProgress', back_populates='user')
    quizzes = relationship('QuizResult', back_populates='user')


class Lesson(Base):
    __tablename__ = 'lessons'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    video_url = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc))

    # Relationship with Milestone
    milestone_id = Column(Integer, ForeignKey('milestones.id'))
    milestone = relationship('Milestone', back_populates='lessons')


class Milestone(Base):
    __tablename__ = 'milestones'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc))

    # Relationship with Lesson
    lessons = relationship('Lesson', back_populates='milestone')
    # Relationship with Badge
    badge = relationship('Badge', uselist=False, back_populates='milestone')


class Badge(Base):
    __tablename__ = 'badges'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc))

    # Relationship with Milestone
    milestone_id = Column(Integer, ForeignKey('milestones.id'))
    milestone = relationship('Milestone', back_populates='badge')


class Quiz(Base):
    __tablename__ = 'quizzes'

    id = Column(Integer, primary_key=True, index=True)
    lesson_id = Column(Integer, ForeignKey('lessons.id'))
    question = Column(Text)
    correct_answer = Column(String)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    # Relationship with Lesson
    lesson = relationship('Lesson', back_populates='quizzes')


class QuizResult(Base):
    __tablename__ = 'quiz_results'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    quiz_id = Column(Integer, ForeignKey('quizzes.id'))
    score = Column(Integer)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    # Relationships
    user = relationship('User', back_populates='quizzes')
    quiz = relationship('Quiz')


class UserProgress(Base):
    __tablename__ = 'user_progress'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    lesson_id = Column(Integer, ForeignKey('lessons.id'))
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc))

    # Relationships
    user = relationship('User', back_populates='progress')
    lesson = relationship('Lesson')


# Additional relationships in Lesson class for Quizzes
Lesson.quizzes = relationship('Quiz', back_populates='lesson')
