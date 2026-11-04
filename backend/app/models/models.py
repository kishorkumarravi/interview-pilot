from datetime import datetime, timezone
from sqlalchemy import (
    Column, Integer, String, Text, Float, Boolean, DateTime,
    ForeignKey, JSON,
)
from sqlalchemy.orm import relationship
from app.core.database import Base


def utcnow():
    return datetime.now(timezone.utc)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=utcnow)


class Lesson(Base):
    __tablename__ = "lessons"
    id = Column(Integer, primary_key=True)
    category = Column(String(50), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    slug = Column(String(200), unique=True, nullable=False)
    difficulty = Column(String(20), default="intermediate")
    order_index = Column(Integer, default=0)
    content = Column(Text, nullable=False)
    examples = Column(JSON, default=list)
    exercises = Column(JSON, default=list)
    tags = Column(JSON, default=list)


class LessonProgress(Base):
    __tablename__ = "lesson_progress"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False)
    completed = Column(Boolean, default=False)
    score = Column(Float, default=0.0)
    completed_at = Column(DateTime)
    time_spent_minutes = Column(Integer, default=0)


class Quiz(Base):
    __tablename__ = "quizzes"
    id = Column(Integer, primary_key=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False)
    question = Column(Text, nullable=False)
    options = Column(JSON, nullable=False)
    correct_index = Column(Integer, nullable=False)
    explanation = Column(Text, default="")


class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"), nullable=False)
    selected_index = Column(Integer, nullable=False)
    is_correct = Column(Boolean, nullable=False)
    attempted_at = Column(DateTime, default=utcnow)


class SystemDesignProblem(Base):
    __tablename__ = "system_design_problems"
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    slug = Column(String(200), unique=True, nullable=False)
    difficulty = Column(String(20), default="medium")
    category = Column(String(50), nullable=False)
    description = Column(Text, nullable=False)
    requirements = Column(JSON, default=dict)
    estimation_hints = Column(JSON, default=dict)
    api_design = Column(JSON, default=dict)
    schema_design = Column(JSON, default=dict)
    scaling_notes = Column(Text, default="")
    failure_modes = Column(JSON, default=list)
    trade_offs = Column(JSON, default=list)
    diagram_description = Column(Text, default="")
    order_index = Column(Integer, default=0)


class SystemDesignAttempt(Base):
    __tablename__ = "system_design_attempts"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    problem_id = Column(Integer, ForeignKey("system_design_problems.id"), nullable=False)
    notes = Column(Text, default="")
    score = Column(Float)
    feedback = Column(Text, default="")
    attempted_at = Column(DateTime, default=utcnow)
    time_spent_minutes = Column(Integer, default=0)


class CodingProblem(Base):
    __tablename__ = "coding_problems"
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    slug = Column(String(200), unique=True, nullable=False)
    difficulty = Column(String(20), nullable=False)
    category = Column(String(50), nullable=False)
    description = Column(Text, nullable=False)
    examples = Column(JSON, default=list)
    constraints = Column(JSON, default=list)
    hints = Column(JSON, default=list)
    solution_java = Column(Text, default="")
    solution_python = Column(Text, default="")
    test_cases = Column(JSON, default=list)
    time_complexity = Column(String(50), default="")
    space_complexity = Column(String(50), default="")
    order_index = Column(Integer, default=0)


class CodingAttempt(Base):
    __tablename__ = "coding_attempts"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    problem_id = Column(Integer, ForeignKey("coding_problems.id"), nullable=False)
    language = Column(String(20), nullable=False)
    code = Column(Text, nullable=False)
    passed = Column(Boolean, default=False)
    attempted_at = Column(DateTime, default=utcnow)


class InterviewSession(Base):
    __tablename__ = "interview_sessions"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    interview_type = Column(String(50), nullable=False)
    topic = Column(String(200), default="")
    status = Column(String(20), default="active")
    overall_score = Column(Float)
    feedback_summary = Column(Text, default="")
    scores = Column(JSON, default=dict)
    started_at = Column(DateTime, default=utcnow)
    ended_at = Column(DateTime)


class InterviewMessage(Base):
    __tablename__ = "interview_messages"
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey("interview_sessions.id"), nullable=False)
    role = Column(String(20), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=utcnow)


class StarQuestion(Base):
    __tablename__ = "star_questions"
    id = Column(Integer, primary_key=True)
    category = Column(String(50), nullable=False)
    question = Column(Text, nullable=False)
    tips = Column(JSON, default=list)
    order_index = Column(Integer, default=0)


class StarAttempt(Base):
    __tablename__ = "star_attempts"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("star_questions.id"), nullable=False)
    situation = Column(Text, default="")
    task = Column(Text, default="")
    action = Column(Text, default="")
    result = Column(Text, default="")
    ai_feedback = Column(Text, default="")
    score = Column(Float)
    attempted_at = Column(DateTime, default=utcnow)


class ProgressSnapshot(Base):
    __tablename__ = "progress_snapshots"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    snapshot_date = Column(DateTime, default=utcnow)
    lessons_completed = Column(Integer, default=0)
    quizzes_passed = Column(Integer, default=0)
    coding_solved = Column(Integer, default=0)
    interviews_done = Column(Integer, default=0)
    total_hours = Column(Float, default=0.0)
    skill_scores = Column(JSON, default=dict)
