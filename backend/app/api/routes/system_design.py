from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth import get_current_user
from app.models import SystemDesignProblem, SystemDesignAttempt
from app.schemas.schemas import (
    SystemDesignProblemOut, SystemDesignProblemSummary, SystemDesignAttemptIn,
)
from app.services.ai_provider import get_ai_provider

router = APIRouter(prefix="/system-design", tags=["system-design"])


@router.get("", response_model=list[SystemDesignProblemSummary])
def list_problems(
    category: str | None = None,
    db: Session = Depends(get_db),
    _user: str = Depends(get_current_user),
):
    q = db.query(SystemDesignProblem)
    if category:
        q = q.filter(SystemDesignProblem.category == category)
    return q.order_by(SystemDesignProblem.order_index).all()


@router.get("/categories")
def list_categories(db: Session = Depends(get_db), _user: str = Depends(get_current_user)):
    rows = db.query(SystemDesignProblem.category).distinct().all()
    return [r[0] for r in rows]


@router.get("/{slug}", response_model=SystemDesignProblemOut)
def get_problem(slug: str, db: Session = Depends(get_db), _user: str = Depends(get_current_user)):
    p = db.query(SystemDesignProblem).filter_by(slug=slug).first()
    if not p:
        raise HTTPException(status_code=404, detail="Problem not found")
    return p


@router.post("/attempt")
def submit_attempt(
    req: SystemDesignAttemptIn,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user),
):
    problem = db.query(SystemDesignProblem).filter_by(id=req.problem_id).first()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")

    provider = get_ai_provider()
    feedback = provider.chat(
        f"You are a system design reviewer. Review this attempt for the problem: {problem.title}",
        [{"role": "user", "content": f"My notes:\n{req.notes}"}],
    )

    attempt = SystemDesignAttempt(
        user_id=int(user_id),
        problem_id=req.problem_id,
        notes=req.notes,
        feedback=feedback,
        score=7.0,
        time_spent_minutes=req.time_spent_minutes,
    )
    db.add(attempt)
    db.commit()
    return {"feedback": feedback, "score": attempt.score}
