from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth import get_current_user
from app.models import CodingProblem, CodingAttempt
from app.schemas.schemas import CodingProblemOut, CodingProblemSummary, CodingAttemptIn

router = APIRouter(prefix="/coding", tags=["coding"])


@router.get("", response_model=list[CodingProblemSummary])
def list_problems(
    category: str | None = None,
    difficulty: str | None = None,
    db: Session = Depends(get_db),
    _user: str = Depends(get_current_user),
):
    q = db.query(CodingProblem)
    if category:
        q = q.filter(CodingProblem.category == category)
    if difficulty:
        q = q.filter(CodingProblem.difficulty == difficulty)
    return q.order_by(CodingProblem.order_index).all()


@router.get("/categories")
def list_categories(db: Session = Depends(get_db), _user: str = Depends(get_current_user)):
    rows = db.query(CodingProblem.category).distinct().all()
    return [r[0] for r in rows]


@router.get("/{slug}", response_model=CodingProblemOut)
def get_problem(slug: str, db: Session = Depends(get_db), _user: str = Depends(get_current_user)):
    p = db.query(CodingProblem).filter_by(slug=slug).first()
    if not p:
        raise HTTPException(status_code=404, detail="Problem not found")
    return p


@router.post("/attempt")
def submit_attempt(
    req: CodingAttemptIn,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user),
):
    problem = db.query(CodingProblem).filter_by(id=req.problem_id).first()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")

    attempt = CodingAttempt(
        user_id=int(user_id),
        problem_id=req.problem_id,
        language=req.language,
        code=req.code,
        passed=True,
    )
    db.add(attempt)
    db.commit()
    return {"status": "submitted", "passed": attempt.passed}
