from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth import get_current_user
from app.models import StarQuestion, StarAttempt
from app.schemas.schemas import StarQuestionOut, StarAttemptIn, StarAttemptOut
from app.services.ai_provider import get_ai_provider

router = APIRouter(prefix="/star", tags=["star"])


@router.get("", response_model=list[StarQuestionOut])
def list_questions(
    category: str | None = None,
    db: Session = Depends(get_db),
    _user: str = Depends(get_current_user),
):
    q = db.query(StarQuestion)
    if category:
        q = q.filter(StarQuestion.category == category)
    return q.order_by(StarQuestion.order_index).all()


@router.get("/categories")
def list_categories(db: Session = Depends(get_db), _user: str = Depends(get_current_user)):
    rows = db.query(StarQuestion.category).distinct().all()
    return [r[0] for r in rows]


@router.post("/attempt", response_model=StarAttemptOut)
def submit_attempt(
    req: StarAttemptIn,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user),
):
    question = db.query(StarQuestion).filter_by(id=req.question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    provider = get_ai_provider()
    prompt = (
        "You are a STAR method behavioural interview coach. "
        "Evaluate the following STAR response and provide actionable feedback with a score out of 10."
    )
    user_content = (
        f"Question: {question.question}\n\n"
        f"Situation: {req.situation}\n"
        f"Task: {req.task}\n"
        f"Action: {req.action}\n"
        f"Result: {req.result}"
    )
    feedback = provider.chat(prompt, [{"role": "user", "content": user_content}])

    import re
    score_match = re.search(r"(\d+(?:\.\d+)?)\s*/\s*10", feedback)
    score = float(score_match.group(1)) if score_match else 7.0

    attempt = StarAttempt(
        user_id=int(user_id),
        question_id=req.question_id,
        situation=req.situation,
        task=req.task,
        action=req.action,
        result=req.result,
        ai_feedback=feedback,
        score=score,
    )
    db.add(attempt)
    db.commit()
    db.refresh(attempt)
    return StarAttemptOut.model_validate(attempt)
