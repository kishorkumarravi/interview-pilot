from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth import get_current_user
from app.models import Lesson, LessonProgress, Quiz, QuizAttempt
from app.schemas.schemas import (
    LessonOut, LessonSummary, LessonProgressIn,
    QuizOut, QuizAnswerIn, QuizAnswerOut,
)
from datetime import datetime, timezone

router = APIRouter(prefix="/lessons", tags=["lessons"])


@router.get("", response_model=list[LessonSummary])
def list_lessons(
    category: str | None = None,
    db: Session = Depends(get_db),
    _user: str = Depends(get_current_user),
):
    q = db.query(Lesson)
    if category:
        q = q.filter(Lesson.category == category)
    return q.order_by(Lesson.category, Lesson.order_index).all()


@router.get("/categories")
def list_categories(db: Session = Depends(get_db), _user: str = Depends(get_current_user)):
    rows = db.query(Lesson.category).distinct().all()
    return [r[0] for r in rows]


@router.get("/{slug}", response_model=LessonOut)
def get_lesson(slug: str, db: Session = Depends(get_db), _user: str = Depends(get_current_user)):
    lesson = db.query(Lesson).filter_by(slug=slug).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson


@router.post("/progress")
def mark_progress(
    req: LessonProgressIn,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user),
):
    prog = db.query(LessonProgress).filter_by(user_id=int(user_id), lesson_id=req.lesson_id).first()
    if prog:
        prog.completed = req.completed
        prog.score = req.score
        prog.time_spent_minutes += req.time_spent_minutes
        if req.completed:
            prog.completed_at = datetime.now(timezone.utc)
    else:
        prog = LessonProgress(
            user_id=int(user_id),
            lesson_id=req.lesson_id,
            completed=req.completed,
            score=req.score,
            time_spent_minutes=req.time_spent_minutes,
            completed_at=datetime.now(timezone.utc) if req.completed else None,
        )
        db.add(prog)
    db.commit()
    return {"status": "ok"}


@router.get("/{slug}/quizzes", response_model=list[QuizOut])
def get_quizzes(slug: str, db: Session = Depends(get_db), _user: str = Depends(get_current_user)):
    lesson = db.query(Lesson).filter_by(slug=slug).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return db.query(Quiz).filter_by(lesson_id=lesson.id).all()


@router.post("/quizzes/answer", response_model=QuizAnswerOut)
def answer_quiz(
    req: QuizAnswerIn,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user),
):
    quiz = db.query(Quiz).filter_by(id=req.quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    is_correct = req.selected_index == quiz.correct_index
    attempt = QuizAttempt(
        user_id=int(user_id),
        quiz_id=quiz.id,
        selected_index=req.selected_index,
        is_correct=is_correct,
    )
    db.add(attempt)
    db.commit()
    return QuizAnswerOut(is_correct=is_correct, correct_index=quiz.correct_index, explanation=quiz.explanation)
