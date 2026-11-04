from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import get_db
from app.core.auth import get_current_user
from app.models import (
    Lesson, LessonProgress, Quiz, QuizAttempt,
    CodingProblem, CodingAttempt,
    InterviewSession, SystemDesignAttempt,
    StarAttempt,
)
from app.schemas.schemas import ProgressOut

router = APIRouter(prefix="/progress", tags=["progress"])


@router.get("", response_model=ProgressOut)
def get_progress(
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user),
):
    uid = int(user_id)
    total_lessons = db.query(Lesson).count()
    lessons_completed = db.query(LessonProgress).filter_by(user_id=uid, completed=True).count()

    total_quizzes = db.query(Quiz).count()
    quizzes_passed = (
        db.query(QuizAttempt.quiz_id)
        .filter_by(user_id=uid, is_correct=True)
        .distinct()
        .count()
    )

    total_coding = db.query(CodingProblem).count()
    coding_solved = (
        db.query(CodingAttempt.problem_id)
        .filter_by(user_id=uid, passed=True)
        .distinct()
        .count()
    )

    interviews_done = db.query(InterviewSession).filter_by(user_id=uid, status="completed").count()

    time_lessons = db.query(func.coalesce(func.sum(LessonProgress.time_spent_minutes), 0)).filter_by(user_id=uid).scalar()
    time_sd = db.query(func.coalesce(func.sum(SystemDesignAttempt.time_spent_minutes), 0)).filter_by(user_id=uid).scalar()
    total_hours = round((time_lessons + time_sd) / 60.0, 1)

    avg_interview = (
        db.query(func.avg(InterviewSession.overall_score))
        .filter(InterviewSession.user_id == uid, InterviewSession.overall_score.isnot(None))
        .scalar()
    )
    avg_star = (
        db.query(func.avg(StarAttempt.score))
        .filter(StarAttempt.user_id == uid, StarAttempt.score.isnot(None))
        .scalar()
    )

    skill_scores = {
        "lessons": round(lessons_completed / max(total_lessons, 1) * 100),
        "coding": round(coding_solved / max(total_coding, 1) * 100),
        "interviews": round(float(avg_interview or 0) * 10),
        "behavioural": round(float(avg_star or 0) * 10),
    }

    recommendations = []
    if lessons_completed < total_lessons * 0.3:
        recommendations.append("Complete more lessons to build foundational knowledge")
    if coding_solved < 10:
        recommendations.append("Practice at least 10 coding problems before interviews")
    if interviews_done < 3:
        recommendations.append("Do more mock interviews to build confidence")
    if not avg_star:
        recommendations.append("Practice STAR responses for behavioural questions")
    if skill_scores["coding"] < 30:
        recommendations.append("Focus on Arrays, Strings, and Trees - most common in interviews")
    if not recommendations:
        recommendations.append("Great progress! Keep practising system design at Staff level")

    return ProgressOut(
        lessons_completed=lessons_completed,
        total_lessons=total_lessons,
        quizzes_passed=quizzes_passed,
        total_quizzes=total_quizzes,
        coding_solved=coding_solved,
        total_coding=total_coding,
        interviews_done=interviews_done,
        total_hours=total_hours,
        skill_scores=skill_scores,
        recommendations=recommendations,
    )
